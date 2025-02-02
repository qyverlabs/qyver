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

from qyver.framework.common.dag.categorical_similarity_node import (
    CategoricalSimilarityNode,
)
from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.data_types import Vector
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.common.transform.transform import Step
from qyver.framework.common.transform.transformation_factory import (
    TransformationFactory,
)
from qyver.framework.online.dag.evaluation_result import EvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode


class OnlineCategoricalSimilarityNode(OnlineNode[CategoricalSimilarityNode, Vector], HasLength):
    def __init__(
        self,
        node: CategoricalSimilarityNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(node, parents, storage_manager)
        self._embedding_transformation = TransformationFactory.create_embedding_transformation(
            self.node.transformation_config
        )

    @property
    @override
    def length(self) -> int:
        return self.node.length

    @property
    def embedding_transformation(self) -> Step[list[str], Vector]:
        return self._embedding_transformation

    @override
    def evaluate_self(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector] | None]:
        if len(self.parents) == 0:
            results = self.load_stored_results_with_default(
                [(parsed_schema.schema, parsed_schema.id_) for parsed_schema in parsed_schemas],
                Vector.init_zero_vector(self.node.length),
            )
        else:
            parent_results = self.evaluate_parent(self.parents[0], parsed_schemas, context)
            results = [self._evaluate_parent_result(parent_result, context) for parent_result in parent_results]
        return [self._wrap_in_evaluation_result(result) for result in results]

    def _evaluate_parent_result(
        self,
        parent_result: EvaluationResult | None,
        context: ExecutionContext,
    ) -> Vector:
        if parent_result is None:
            return Vector.init_zero_vector(self.node.length)
        input_ = parent_result.main.value
        categories = input_ if isinstance(input_, list) else [input_]
        return self.embedding_transformation.transform(categories, context)
