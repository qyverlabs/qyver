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


from pathlib import Path

import structlog
from beartype.typing import Sequence
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.data_types import Vector
from qyver.framework.common.space.config.embedding.text_similarity_embedding_config import (
    TextSimilarityEmbeddingConfig,
)
from qyver.framework.common.space.embedding.embedding import Embedding
from qyver.framework.common.space.embedding.embedding_cache import EmbeddingCache
from qyver.framework.common.space.embedding.sentence_transformer_manager import (
    SentenceTransformerManager,
)

logger = structlog.getLogger()


class SentenceTransformerEmbedding(Embedding[str, TextSimilarityEmbeddingConfig]):
    def __init__(
        self,
        embedding_config: TextSimilarityEmbeddingConfig,
        model_cache_dir: Path | None = None,
    ) -> None:
        super().__init__(embedding_config)
        self.manager = SentenceTransformerManager(self._config.model_name, model_cache_dir)
        self._cache = EmbeddingCache(self._config.cache_size)

    @override
    def embed_multiple(self, inputs: Sequence[str], context: ExecutionContext) -> list[Vector]:
        cache_info = self._cache.calculate_cache_info(inputs)
        new_vectors = self.manager.embed_text(cache_info.inputs_to_embed, context)
        self._cache.update(cache_info.inputs_to_embed, new_vectors)
        combined_vectors = cache_info.combine_vectors(new_vectors)
        return combined_vectors

    @override
    def embed(self, input_: str, context: ExecutionContext) -> Vector:
        return self.embed_multiple([input_], context)[0]

    @property
    @override
    def length(self) -> int:
        return self._config.length
