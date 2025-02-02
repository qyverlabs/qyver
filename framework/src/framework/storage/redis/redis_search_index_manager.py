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


import redis
import redis.client
from beartype.typing import Sequence, cast
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from typing_extensions import override

from qyver.framework.common.storage.index_config import IndexConfig
from qyver.framework.common.storage.search_index.manager.dynamic_search_index_manager import (
    DynamicSearchIndexManager,
)
from qyver.framework.common.storage.search_index.search_algorithm import (
    SearchAlgorithm,
)
from qyver.framework.storage.redis.redis_field_descriptor_compiler import (
    RedisFieldDescriptorCompiler,
)
from qyver.framework.storage.redis.redis_field_encoder import RedisFieldEncoder


class RedisSearchIndexManager(DynamicSearchIndexManager):
    def __init__(
        self,
        client: redis.Redis,
        encoder: RedisFieldEncoder,
        index_configs: Sequence[IndexConfig] | None = None,
    ) -> None:
        super().__init__(index_configs)
        self._client = client
        self._encoder = encoder

    @override
    @property
    def supported_vector_indexing(self) -> Sequence[SearchAlgorithm]:
        return [SearchAlgorithm.FLAT, SearchAlgorithm.HNSW]

    @override
    def _list_search_index_names_from_vdb(self, collection_name: str) -> Sequence[str]:
        return list(
            self._encoder._decode_string(cast(bytes, index_name))
            for index_name in self._client.execute_command("FT._LIST")
        )

    @override
    def _create_search_index(self, index_config: IndexConfig, collection_name: str) -> None:
        index_def = IndexDefinition(index_type=IndexType.HASH)
        fields = RedisFieldDescriptorCompiler.compile_descriptors(
            index_config.vector_field_descriptor, index_config.field_descriptors
        )
        self._client.ft(index_config.index_name).create_index(
            list(fields),
            definition=index_def,
            stopwords=[],  # otherwise queries will not work with words like "no" or "a"
        )

    @override
    def drop_search_index(self, index_name: str, collection_name: str) -> None:
        self._client.ft(index_name).dropindex()
        self._index_configs.pop(index_name, None)
