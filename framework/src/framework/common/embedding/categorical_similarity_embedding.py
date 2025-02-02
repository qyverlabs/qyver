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


import numpy as np
from beartype.typing import Sequence
from typing_extensions import TypeVar, override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.data_types import NPArray, Vector
from qyver.framework.common.embedding.embedding import Embedding
from qyver.framework.common.space.config.categorical_similarity_embedding_config import (
    CategoricalSimilarityEmbeddingConfig,
)
from qyver.framework.common.space.normalization import L2Norm

CATEGORICAL_ENCODING_VALUE: int = 1

CategoryT = TypeVar("CategoryT", str, list[str])


class CategoricalSimilarityEmbedding(
    Embedding[CategoryT, CategoricalSimilarityEmbeddingConfig]
):
    def __init__(self, embedding_config: CategoricalSimilarityEmbeddingConfig) -> None:
        super().__init__(embedding_config)
        self._other_category_index: int | None = (
            self.length - 1 if self._config.uncategorized_as_category else None
        )
        self._category_index_map: dict[str, int] = {
            elem: i for i, elem in enumerate(self._config.categories)
        }
        self._default_n_hot_encoding = np.full(
            self.length, self._config.negative_filter, dtype=np.float64
        )
        self._normalization = L2Norm()

    @property
    @override
    def normalization(self) -> L2Norm:
        return self._normalization

    @override
    def embed(self, input_: list[str] | str, context: ExecutionContext) -> Vector:
        inputs: list[str] = input_ if isinstance(input_, list) else [input_]
        n_hot_encoding: NPArray = self._n_hot_encode(inputs, context.is_query_context)
        negative_filter_indices = set(
            i for i in range(self.length) if i not in self._get_category_indices(inputs)
        )
        vector = Vector(n_hot_encoding, negative_filter_indices)
        return self.normalization.normalize(vector)

    def _n_hot_encode(self, category_list: Sequence[str], is_query: bool) -> NPArray:
        n_hot_encoding = self._default_n_hot_encoding.copy()
        if is_query:
            n_hot_encoding.fill(0)
        category_indices = self._get_category_indices(category_list)
        if category_indices:
            n_hot_encoding[category_indices] = CATEGORICAL_ENCODING_VALUE
        return n_hot_encoding

    def _get_category_indices(self, text_input: Sequence[str]) -> list[int]:
        return list(
            {
                category_index
                for category_value in text_input
                if (category_index := self._get_index_for_category(category_value))
                is not None
            }
        )

    def _get_index_for_category(self, category: str) -> int | None:
        return self._category_index_map.get(category, self._other_category_index)

    @property
    @override
    def length(self) -> int:
        return self._config.length
