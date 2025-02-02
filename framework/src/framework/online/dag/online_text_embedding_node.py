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

from __future__ import annotations

from beartype.typing import Sequence
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.text_embedding_node import TextEmbeddingNode
from qyver.framework.common.data_types import Vector
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.common.transform.transform import Step
from qyver.framework.common.transform.transformation_factory import (
    TransformationFactory,
)
from qyver.framework.online.dag.default_online_node import DefaultOnlineNode
from qyver.framework.online.dag.evaluation_result import SingleEvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode


class OnlineTextEmbeddingNode(DefaultOnlineNode[TextEmbeddingNode, Vector], HasLength):
    def __init__(
        self,
        node: TextEmbeddingNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(node, parents, storage_manager)
        self._embedding_transformation = self._init_embedding_transformation()

    def _init_embedding_transformation(self) -> Step[Sequence[str], list[Vector]]:
        return TransformationFactory.create_multi_embedding_transformation(self.node.transformation_config)

    @property
    @override
    def length(self) -> int:
        return self.node.length

    @property
    def embedding_transformation(self) -> Step[Sequence[str], list[Vector]]:
        return self._embedding_transformation

    @override
    def get_fallback_result(self, parsed_schema: ParsedSchema) -> Vector:
        stored_result = self.load_stored_result(parsed_schema.schema, parsed_schema.id_)
        if stored_result is not None:
            return stored_result
        return Vector.init_zero_vector(self.node.length)

    @override
    def _evaluate_singles(
        self,
        parent_results: Sequence[dict[OnlineNode, SingleEvaluationResult[str]]],
        context: ExecutionContext,
    ) -> Sequence[Vector | None]:
        none_indices = [i for i, parent_result in enumerate(parent_results) if not parent_result]
        non_none_parent_results = [parent_result for parent_result in parent_results if parent_result]
        input_ = list(
            map(
                lambda parent_result: list(parent_result.values())[0].value,
                non_none_parent_results,
            )
        )
        embedded_texts: list[Vector | None] = list(self.__embed_texts(input_, context))
        for i in none_indices:
            embedded_texts.insert(i, None)
        return embedded_texts

    def __embed_texts(self, texts: Sequence[str], context: ExecutionContext) -> list[Vector]:
        return self.embedding_transformation.transform(texts, context)
