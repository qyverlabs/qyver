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


from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.data_types import Vector
from qyver.framework.common.embedding.embedding import Embedding
from qyver.framework.common.space.config.custom_embedding_config import (
    CustomEmbeddingConfig,
)
from qyver.framework.common.space.normalization import L2Norm, Normalization


class CustomEmbedding(Embedding[Vector, CustomEmbeddingConfig]):
    def __init__(self, embedding_config: CustomEmbeddingConfig) -> None:
        super().__init__(embedding_config)
        self._normalization = L2Norm()

    @property
    @override
    def normalization(self) -> Normalization:
        return self._normalization

    @property
    @override
    def length(self) -> int:
        return self._config.length

    @override
    def embed(self, input_: Vector, context: ExecutionContext) -> Vector:
        return self.normalization.normalize(input_)
