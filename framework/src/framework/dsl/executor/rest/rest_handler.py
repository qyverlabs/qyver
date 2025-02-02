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

from beartype.typing import Sequence, TypeVar
from furl import furl

from qyver.framework.dsl.executor.exception import DuplicateEndpointException
from qyver.framework.dsl.executor.rest.rest_configuration import (
    RestEndpointConfiguration,
    RestQuery,
)
from qyver.framework.dsl.query.query_mixin import QueryMixin
from qyver.framework.dsl.query.result import QueryResult
from qyver.framework.dsl.source.rest_source import RestSource

REST = TypeVar("REST", RestSource, RestQuery)


class RestHandler:
    def __init__(
        self,
        query_mixin: QueryMixin,
        sources: Sequence[RestSource],
        queries: Sequence[RestQuery],
        endpoint_config: RestEndpointConfiguration,
    ) -> None:
        self.__query_mixin = query_mixin
        self.__path_to_source_map: dict[str, RestSource] = self.__create_path_to_resource_mapping(
            sources,
            endpoint_config.api_root_path,
            endpoint_config.ingest_path_prefix,
        )
        self.__path_to_query_map: dict[str, RestQuery] = self.__create_path_to_resource_mapping(
            queries,
            endpoint_config.api_root_path,
            endpoint_config.query_path_prefix,
        )

    @property
    def ingest_paths(self) -> list[str]:
        return list(self.__path_to_source_map.keys())

    @property
    def query_paths(self) -> list[str]:
        return list(self.__path_to_query_map.keys())

    def _ingest_handler(self, input_schema: dict, path: str) -> None:
        source = self.__path_to_source_map[path]
        source.put([input_schema])

    def _query_handler(self, query_descriptor: dict, path: str) -> QueryResult:
        query = self.__path_to_query_map[path].query_descriptor
        return self.__query_mixin.query(query, **query_descriptor)

    def __create_path_to_resource_mapping(
        self,
        resources: Sequence[REST],
        api_root_path: str,
        path_prefix: str,
    ) -> dict[str, REST]:
        path_to_resource = {}
        for resource in resources:
            path_string = str(
                furl(path=api_root_path).path.add(path_prefix).add(resource.path)  # type: ignore[arg-type]
            )
            if path_string in path_to_resource:
                raise DuplicateEndpointException(
                    f"Endpoint duplication detected. The path: {path_string} has been previously added."
                )
            path_to_resource[path_string] = resource
        return path_to_resource
