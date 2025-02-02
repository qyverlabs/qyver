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

from beartype.typing import Any, Sequence

from qyver.framework.common.exception import QueryException
from qyver.framework.common.util.type_validator import TypeValidator
from qyver.framework.dsl.executor.query.query_executor import QueryExecutor
from qyver.framework.dsl.index.index import Index
from qyver.framework.dsl.query.query_descriptor import QueryDescriptor
from qyver.framework.dsl.query.query_result_converter.query_result_converter import (
    QueryResultConverter,
)
from qyver.framework.dsl.query.query_vector_factory import QueryVectorFactory
from qyver.framework.dsl.query.result import QueryResult


@TypeValidator.wrap
class QueryMixin:
    """
    A mixin class that provides query execution capabilities for classes that include it.
    This class sets up the necessary infrastructure to execute queries on a set of indices
    using a storage manager.
    """

    def setup_query_execution(self, indices: Sequence[Index]) -> None:
        """
        Set up the query execution environment by initializing a mapping between indices
        and their corresponding QueryVectorFactory instances.

        Args:
            indices (Sequence[Index]): A sequence of Index instances to be used for query execution.
            storage_manager (StorageManager): The storage manager instance to be used.
        """
        self._query_vector_factory_by_index = {index: QueryVectorFactory(index._dag) for index in indices}

    def setup_query_result_converter(self, query_result_converter: QueryResultConverter) -> None:
        """
        Set up the query result converter to be used for converting the query results.

        Args:
            query_result_converter (QueryResultConverter): The query result converter instance.
        """
        self._query_result_converter = query_result_converter

    def query(self, query_descriptor: QueryDescriptor, **params: Any) -> QueryResult:
        """
        Execute a query using the provided QueryDescriptor and additional parameters.

        Args:
            query_descriptor (QueryDescriptor): The query object containing the query details.
            **params (Any): Additional parameters for the query execution.

        Returns:
            Result: The result of the query execution.

        Raises:
            QueryException: If the query index is not found among the executor's indices.
        """
        if query_vector_factory := self._query_vector_factory_by_index.get(query_descriptor.index):
            # 'self' is an App instance; MyPy can't infer the inheriting class. See [FAI-2085].
            query_result: QueryResult = QueryExecutor(
                self, query_descriptor, query_vector_factory  # type: ignore
            ).query(**params)
            return self._query_result_converter.convert(query_result)

        raise QueryException(
            (
                f"Query index {query_descriptor.index} is not amongst the executor's indices: ",
                f" {list(self._query_vector_factory_by_index.keys())}",
            )
        )
