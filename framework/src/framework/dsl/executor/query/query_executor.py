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


from collections import defaultdict
from functools import partial

import numpy as np
import structlog
from beartype.typing import Any, Sequence, cast

from qyver.framework.common.dag.context import (
    CONTEXT_COMMON,
    CONTEXT_COMMON_NOW,
    ExecutionContext,
    ExecutionEnvironment,
    NowStrategy,
)
from qyver.framework.common.data_types import NodeDataTypes, Vector
from qyver.framework.common.exception import QueryException
from qyver.framework.common.interface.weighted import Weighted
from qyver.framework.common.storage_manager.knn_search_params import (
    KNNSearchParams,
)
from qyver.framework.common.storage_manager.search_result_item import (
    SearchResultItem,
)
from qyver.framework.dsl.executor.executor import App
from qyver.framework.dsl.query.param import ParamInputType
from qyver.framework.dsl.query.query_clause import (
    LooksLikeFilterClause,
    SimilarFilterClause,
)
from qyver.framework.dsl.query.query_descriptor import QueryDescriptor
from qyver.framework.dsl.query.query_param_value_setter import (
    QueryParamValueSetter,
)
from qyver.framework.dsl.query.query_vector_factory import QueryVectorFactory
from qyver.framework.dsl.query.result import (
    QueryResult,
    ResultEntry,
    ResultEntryMetadata,
    ResultMetadata,
)
from qyver.framework.query.query_node_input import QueryNodeInput

logger = structlog.getLogger()


class QueryExecutor:
    """
    QueryExecutor provides an interface to execute predefined queries with query time parameters.
    """

    def __init__(
        self,
        app: App,
        query_descriptor: QueryDescriptor,
        query_vector_factory: QueryVectorFactory,
    ) -> None:
        """
        Initializes the QueryExecutor.

        Args:
            app: An instance of the App class.
            query_descriptor: An instance of the QueryDescriptor class representing the query to be executed.
            evaluator: An instance of the QueryDagEvaluator class used to evaluate the query.
        """
        self.app = app
        self._query_descriptor = query_descriptor
        self.query_vector_factory = query_vector_factory
        self._logger = logger.bind(schema=self._query_descriptor.schema._schema_name)

    def query(self, **params: ParamInputType) -> QueryResult:
        """
        Execute a query with keyword parameters.

        Args:
            **params: Arbitrary arguments with keys corresponding to the `name` attribute of the `Param` instance.

        Returns:
            Result: The result of the query execution that can be inspected and post-processed.

        Raises:
            QueryException: If the query index is not amongst the executor's indices.
        """
        self.__check_executor_has_index()
        query_descriptor: QueryDescriptor = QueryParamValueSetter.set_values(self._query_descriptor, params)
        knn_search_params = self._produce_knn_search_params(query_descriptor)
        entities = self._knn_search(knn_search_params, query_descriptor)
        self._logger.info(
            "executed query",
            n_results=len(entities),
            limit=knn_search_params.limit,
            radius=knn_search_params.radius,
            pii_knn_params=params,
            pii_query_vector=partial(str, knn_search_params.vector),
        )
        metadata = ResultMetadata(
            schema_name=query_descriptor.schema._schema_name,
            search_vector=[float(x) for x in knn_search_params.vector.value.tolist()],
            search_params=self._map_search_params(query_descriptor),
        )
        return QueryResult(entries=self._map_entities(entities), metadata=metadata)

    def _map_entities(self, entities: Sequence[SearchResultItem]) -> list[ResultEntry]:
        return [
            ResultEntry(
                id=entity.header.origin_id or entity.header.object_id,
                fields={field.schema_field.name: field.value for field in entity.fields},
                metadata=ResultEntryMetadata(score=entity.score),
            )
            for entity in entities
        ]

    def _map_search_params(self, query_descriptor: QueryDescriptor) -> dict[str, Any]:
        value_by_param_name = {clause.value_param_name: clause.get_value() for clause in query_descriptor.clauses}
        weight_by_param_name = {
            clause.weight_param_name: clause.get_weight() for clause in query_descriptor.get_weighted_clauses()
        }
        return {**value_by_param_name, **weight_by_param_name}

    def _produce_knn_search_params(self, query_descriptor: QueryDescriptor) -> KNNSearchParams:
        limit = query_descriptor.get_limit()
        radius = query_descriptor.get_radius()
        schema_fields_to_return = query_descriptor.get_selected_fields()
        hard_filters = query_descriptor.get_hard_filters()
        query_vector = self._produce_query_vector(query_descriptor)
        return KNNSearchParams(query_vector, limit, hard_filters, schema_fields_to_return, radius)

    def _produce_query_vector(self, query_descriptor: QueryDescriptor) -> Vector:
        weight_by_space = query_descriptor.get_weights_by_space()
        context = self._create_query_context_base(query_descriptor)
        query_node_inputs_by_node_id = self.calculate_query_node_inputs_by_node_id(query_descriptor)
        return self.query_vector_factory.produce_vector(
            query_descriptor.index._node_id,
            query_node_inputs_by_node_id,
            weight_by_space,
            query_descriptor.schema,
            context,
        )

    def _create_query_context_base(self, query_descriptor: QueryDescriptor) -> ExecutionContext:
        eval_context = ExecutionContext(
            environment=ExecutionEnvironment.QUERY,
            data=self.app._context.data,
            now_strategy=NowStrategy.CONTEXT_TIME,
        )
        context_time = query_descriptor.get_context_time(self.app._context.now())
        eval_context.update_data({CONTEXT_COMMON: {CONTEXT_COMMON_NOW: context_time}})
        return eval_context

    def calculate_query_node_inputs_by_node_id(
        self, query_descriptor: QueryDescriptor
    ) -> dict[str, list[QueryNodeInput]]:
        inputs: defaultdict = defaultdict(list)

        def add_input(
            node_id: str,
            value: Any,
            weight: float,
            to_invert: bool,
        ) -> None:
            inputs[node_id].append(
                QueryNodeInput(
                    Weighted(cast(NodeDataTypes, value), weight),
                    to_invert,
                )
            )

        looks_like_clause = query_descriptor.get_clause_by_type(LooksLikeFilterClause)
        if looks_like_clause and looks_like_clause.evaluate():
            index_node_id = query_descriptor.index._node_id
            if vector := self.__get_looks_like_vector(index_node_id, looks_like_clause):
                add_input(index_node_id, vector, looks_like_clause.get_weight(), True)
        for similar_clause in query_descriptor.get_clauses_by_type(SimilarFilterClause):
            if (result := similar_clause.evaluate()) is not None:
                node_id = similar_clause.space._get_embedding_node(query_descriptor.schema).node_id
                _, weighted_value = result
                add_input(
                    node_id,
                    similar_clause.field_set._generate_space_input(weighted_value.item),
                    weighted_value.weight,
                    False,
                )

        return inputs

    def __get_looks_like_vector(
        self,
        index_node_id: str,
        looks_like_clause: LooksLikeFilterClause,
    ) -> Vector:
        object_id = str(looks_like_clause.get_value())
        vector: Vector | None = self.app._storage_manager.read_node_result(
            looks_like_clause.schema_field.schema_obj,
            object_id,
            index_node_id,
            Vector,
        )
        if vector is None:
            raise QueryException(f"Entity not found object_id: {object_id} node_id: {index_node_id}")
        return vector

    def _knn_search(
        self, knn_search_params: KNNSearchParams, query_descriptor: QueryDescriptor
    ) -> Sequence[SearchResultItem]:
        return self.app.storage_manager.knn_search(
            query_descriptor.index._node, query_descriptor.schema, knn_search_params
        )

    def _calculate_partial_scores(self, query_vector: Vector, result_vectors: Sequence[Vector]) -> list[list[float]]:
        lengths = [space.length for space in self._query_descriptor.index._spaces]
        all_vectors = list(result_vectors) + [query_vector]
        vectors_parts = [[part.value for part in vector.split(lengths)] for vector in all_vectors]
        vector_parts_per_space = [
            np.array([vectors_part[i] for vectors_part in vectors_parts]) for i in range(len(lengths))
        ]
        result_count = len(result_vectors)
        per_space_scores = [
            list[float](np.dot(vector_parts[:result_count], vector_parts[result_count]))
            for vector_parts in vector_parts_per_space
        ]
        return [[scores[i] for scores in per_space_scores] for i in range(result_count)]

    def __check_executor_has_index(self) -> None:
        if self._query_descriptor.index not in self.app._indices:
            raise QueryException(
                f"Query index {self._query_descriptor.index} is not amongst "
                + f"the executor's indices {self.app._indices}"
            )
