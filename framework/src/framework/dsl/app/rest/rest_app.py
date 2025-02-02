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


from beartype.typing import Sequence

from qyver.framework.blob.blob_handler import BlobHandler
from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.settings import Settings
from qyver.framework.dsl.app.online.online_app import OnlineApp
from qyver.framework.dsl.executor.rest.rest_configuration import (
    RestEndpointConfiguration,
    RestQuery,
)
from qyver.framework.dsl.executor.rest.rest_handler import RestHandler
from qyver.framework.dsl.index.index import Index
from qyver.framework.dsl.query.query_result_converter.serializable_query_result_converter import (
    SerializableQueryResultConverter,
)
from qyver.framework.dsl.source.data_loader_source import DataLoaderSource
from qyver.framework.dsl.source.rest_source import RestSource
from qyver.framework.dsl.storage.vector_database import VectorDatabase
from qyver.framework.queue.interface.queue import Queue
from qyver.framework.queue.interface.queue_message import MessageBody


class RestApp(OnlineApp[RestSource | DataLoaderSource]):
    """
    Rest implementation of the App class.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        sources: Sequence[RestSource | DataLoaderSource],
        indices: Sequence[Index],
        queries: Sequence[RestQuery],
        vector_database: VectorDatabase,
        context: ExecutionContext,
        endpoint_configuration: RestEndpointConfiguration,
        queue: Queue[MessageBody[dict]] | None = None,
        blob_handler: BlobHandler | None = None,
    ):
        """
        Initialize the RestApp from a RestExecutor.

        Args:
            sources (Sequence[RestSource | DataLoaderSource]): The list of sources, which can be either
                RestSource or DataLoaderSource.
            indices (Sequence[Index]): The list of indices to be used by the RestApp.
            queries (Sequence[RestQuery]): The list of queries to be executed by the RestApp.
            vector_database (VectorDatabase): The vector database instance to be used by the RestApp.
            context (ExecutionContext): The execution context for the RestApp.
            endpoint_configuration (RestEndpointConfiguration): The configuration for the REST endpoints.
            queue (Queue[dict] | None): a messaging queue persisting the ingested data; defaults to None.
        """
        super().__init__(
            sources,
            indices,
            vector_database,
            context,
            Settings().INIT_SEARCH_INDICES,
            queue,
            blob_handler,
            SerializableQueryResultConverter(),
        )
        self._endpoint_configuration = endpoint_configuration
        self._queries = queries

        self.__data_loader_sources = [source for source in self._sources if isinstance(source, DataLoaderSource)]

        self.__rest_handler = RestHandler(
            self,
            [source for source in self._sources if isinstance(source, RestSource)],
            self._queries,
            self._endpoint_configuration,
        )

    @property
    def data_loader_sources(self) -> Sequence[DataLoaderSource]:
        """
        Property that returns the list of DataLoaderSource instances associated with the RestApp.

        Returns:
            Sequence[DataLoaderSource]: A sequence of DataLoaderSource instances.
        """
        return self.__data_loader_sources

    @property
    def handler(self) -> RestHandler:
        """
        Property that returns the RestHandler instance associated with the RestApp.

        Returns:
            RestHandler: An instance of RestHandler.
        """
        return self.__rest_handler
