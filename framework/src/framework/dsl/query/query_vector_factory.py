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

from collections.abc import Mapping

from beartype.typing import Sequence

from qyver.framework.common.dag.context import (
    ExecutionContext,
    ExecutionEnvironment,
    NowStrategy,
)
from qyver.framework.common.dag.dag import Dag
from qyver.framework.common.data_types import Vector
from qyver.framework.common.schema.id_schema_object import IdSchemaObject
from qyver.framework.dsl.query.query_weighting import QueryWeighting
from qyver.framework.dsl.space.space import Space
from qyver.framework.query.dag.query_index_node import (
    QUERIED_SCHEMA_NAME_CONTEXT_KEY,
)
from qyver.framework.query.query_dag_evaluator import QueryDagEvaluator
from qyver.framework.query.query_node_input import QueryNodeInput

# Exclude from documentation.
__pdoc__ = {}
__pdoc__["QueryVectorFactory"] = False


class QueryVectorFactory:
    def __init__(self, dag: Dag) -> None:
        self._evaluator = QueryDagEvaluator(dag)
        self._query_weighting = QueryWeighting(dag)

    def produce_vector(
        self,
        index_node_id: str,
        query_node_inputs_by_node_id: Mapping[str, Sequence[QueryNodeInput]],
        global_space_weight_map: dict[Space, float],
        schema: IdSchemaObject,
        context_base: ExecutionContext,
    ) -> Vector:
        space_node_id_weight_map: dict[str, float] = self.__get_node_id_weight_map_from_space_weight_map(
            schema, global_space_weight_map
        )
        context = self._create_query_context(context_base, index_node_id, schema._schema_name, space_node_id_weight_map)
        result = self._evaluator.evaluate(query_node_inputs_by_node_id, context)
        return result

    def _create_query_context(
        self,
        context_base: ExecutionContext,
        index_node_id: str,
        schema_name: str,
        node_id_weight_map: dict[str, float],
    ) -> ExecutionContext:
        eval_context = ExecutionContext(
            environment=ExecutionEnvironment.QUERY,
            data=context_base.data,
            now_strategy=NowStrategy.CONTEXT_TIME,
        )
        eval_context.update_data(self._query_weighting.get_node_weights(node_id_weight_map))
        eval_context.set_node_context_value(index_node_id, QUERIED_SCHEMA_NAME_CONTEXT_KEY, schema_name)
        return eval_context

    @staticmethod
    def __get_node_id_weight_map_from_space_weight_map(
        schema: IdSchemaObject, space_weight_map: dict[Space, float]
    ) -> dict[str, float]:
        return {space._get_embedding_node(schema).node_id: weight for space, weight in space_weight_map.items()}
