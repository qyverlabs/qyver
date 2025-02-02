# Copyright 2024 qyver, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from functools import partial

import structlog

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.dag import Dag
from qyver.framework.common.data_types import Vector
from qyver.framework.common.exception import (
    DagEvaluationException,
    InvalidSchemaException,
)
from qyver.framework.common.parser.parsed_schema import (
    ParsedSchema,
    ParsedSchemaWithEvent,
)
from qyver.framework.common.schema.id_schema_object import IdSchemaObject
from qyver.framework.common.schema.schema_object import SchemaObject
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.compiler.online.online_schema_dag_compiler import (
    OnlineSchemaDagCompiler,
)
from qyver.framework.online.dag.evaluation_result import EvaluationResult
from qyver.framework.online.dag.online_schema_dag import OnlineSchemaDag

logger = structlog.get_logger()


class QueryDagEvaluator:
    def __init__(
        self,
        dag: Dag,
        schemas: set[SchemaObject],
        storage_manager: StorageManager,
    ) -> None:
        self._dag = dag
        self._schemas = schemas
        self._schema_online_schema_dag_mapper = (
            self.__init_schema_online_schema_dag_mapper(
                self._schemas, self._dag, storage_manager
            )
        )
        for schema, online_schema_dag in self._schema_online_schema_dag_mapper.items():
            logger.info(
                "initialized entity dag",
                schema=schema._schema_name,
                node_ids=[node.node_id for node in online_schema_dag.nodes],
                node_types=[node.class_name for node in online_schema_dag.nodes],
            )

    def __get_single_schema(self, parsed_schemas: list[ParsedSchema]) -> IdSchemaObject:
        unique_schemas: set[IdSchemaObject] = {
            parsed_schema.schema for parsed_schema in parsed_schemas
        }
        if len(unique_schemas) != 1:
            raise InvalidSchemaException(
                f"Multiple schemas ({[s._schema_name for s in unique_schemas]}) present in the index."
            )
        return next(iter(unique_schemas))

    def evaluate(
        self,
        parsed_schemas: list[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector]]:
        index_schema = self.__get_single_schema(parsed_schemas)
        if (
            online_schema_dag := self._schema_online_schema_dag_mapper.get(index_schema)
        ) is not None:
            results = online_schema_dag.evaluate(parsed_schemas, context)
            for i, result in enumerate(results):
                logger.info(
                    "evaluated entity",
                    schema=index_schema._schema_name,
                    pii_vector=partial(str, result.main.value),
                    pii_field_values=[
                        field.value for field in parsed_schemas[i].fields
                    ],
                )
            return results

        raise InvalidSchemaException(
            f"Schema ({index_schema._schema_name}) isn't present in the index."
        )

    def _log_evaluated_event(
        self, parsed_schema_with_event: ParsedSchemaWithEvent, result: EvaluationResult
    ) -> None:
        logger.info(
            "evaluated event",
            event_id=parsed_schema_with_event.event_parsed_schema.id_,
            affected_schema=parsed_schema_with_event.schema._schema_name,
            affecting_schema=parsed_schema_with_event.event_parsed_schema.schema._schema_name,
            pii_event_vector=partial(str, result.main.value),
            pii_field_values=[
                field.value
                for field in parsed_schema_with_event.event_parsed_schema.fields
            ],
        )

    def __init_schema_online_schema_dag_mapper(
        self,
        schemas: set[SchemaObject],
        dag: Dag,
        storage_manager: StorageManager,
    ) -> dict[SchemaObject, OnlineSchemaDag]:
        return {
            schema: OnlineSchemaDagCompiler(set(dag.nodes)).compile_schema_dag(
                dag.project_to_schema(schema),
                storage_manager,
            )
            for schema in schemas
        }

    def evaluate_single(
        self,
        parsed_schema: ParsedSchema,
        context: ExecutionContext,
    ) -> EvaluationResult[Vector]:
        result = self.evaluate([parsed_schema], context)[0]
        QueryDagEvaluator.__check_evaluation(result)
        return result

    @staticmethod
    def __check_evaluation(evaluation: EvaluationResult[Vector]) -> None:
        if len(evaluation.chunks) > 0:
            raise DagEvaluationException(
                "Evaluation cannot have chunked parts in query context."
            )

    def re_weight_vector(
        self,
        schema: SchemaObject,
        vector: Vector,
        context: ExecutionContext,
    ) -> Vector:
        if (
            online_schema_dag := self._schema_online_schema_dag_mapper.get(schema)
        ) is not None:
            return online_schema_dag.leaf_node._re_weight_vector(
                schema, vector, context
            )
        raise InvalidSchemaException(
            f"Schema ({schema._schema_name}) isn't present in the index."
        )
