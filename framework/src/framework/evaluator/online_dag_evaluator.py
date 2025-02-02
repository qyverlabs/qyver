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
from qyver.framework.common.dag.dag_effect import DagEffect
from qyver.framework.common.data_types import Vector
from qyver.framework.common.exception import (
    InvalidDagEffectException,
    InvalidSchemaException,
)
from qyver.framework.common.parser.parsed_schema import (
    ParsedSchema,
    ParsedSchemaWithEvent,
)
from qyver.framework.common.schema.id_schema_object import IdSchemaObject
from qyver.framework.common.schema.schema_object import SchemaObject
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.compiler.online_schema_dag_compiler import (
    OnlineSchemaDagCompiler,
)
from qyver.framework.evaluator.dag_evaluator import DagEvaluator
from qyver.framework.online.dag.evaluation_result import EvaluationResult
from qyver.framework.online.dag.online_schema_dag import OnlineSchemaDag

logger = structlog.get_logger()


class OnlineDagEvaluator(DagEvaluator[EvaluationResult[Vector]]):
    def __init__(
        self,
        dag: Dag,
        schemas: set[SchemaObject],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__()
        self._dag = dag
        self._schemas = schemas
        self._schema_online_schema_dag_mapper = (
            self.__init_schema_online_schema_dag_mapper(
                self._schemas, self._dag, storage_manager
            )
        )
        self._dag_effect_online_schema_dag_mapper = (
            self.__init_dag_effect_online_schema_dag_mapper(self._dag, storage_manager)
        )
        self._log_dag_init()

    def _log_dag_init(self) -> None:
        for schema, online_schema_dag in self._schema_online_schema_dag_mapper.items():
            logger.info(
                "initialized entity dag",
                schema=schema._schema_name,
                node_ids=[node.node_id for node in online_schema_dag.nodes],
                node_types=[node.class_name for node in online_schema_dag.nodes],
            )
        for (
            dag_effect,
            online_schema_dag,
        ) in self._dag_effect_online_schema_dag_mapper.items():
            logger.info(
                "initialized event dag",
                affected_schema=dag_effect.resolved_affected_schema_reference.schema._schema_name,
                affecting_schema=dag_effect.resolved_affecting_schema_reference.schema._schema_name,
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

    def evaluate_by_dag_effect(
        self,
        parsed_schema_with_event: ParsedSchemaWithEvent,
        context: ExecutionContext,
        dag_effect: DagEffect,
    ) -> EvaluationResult[Vector]:
        if (
            online_schema_dag := self._dag_effect_online_schema_dag_mapper.get(
                dag_effect
            )
        ) is not None:
            result = online_schema_dag.evaluate([parsed_schema_with_event], context)[0]
            self._log_evaluated_event(parsed_schema_with_event, result)
            return result
        raise InvalidDagEffectException(
            f"DagEffect ({dag_effect}) isn't present in the index."
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

    def __init_dag_effect_online_schema_dag_mapper(
        self, dag: Dag, storage_manager: StorageManager
    ) -> dict[DagEffect, OnlineSchemaDag]:
        dag_effect_schema_dag_map = {
            dag_effect: dag.project_to_dag_effect(dag_effect)
            for dag_effect in dag.dag_effects
        }
        return {
            dag_effect: OnlineSchemaDagCompiler(
                set(schema_dag.nodes)
            ).compile_schema_dag(
                schema_dag,
                storage_manager,
            )
            for dag_effect, schema_dag in dag_effect_schema_dag_map.items()
        }
