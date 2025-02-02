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

from beartype.typing import cast
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.custom_node import CustomVectorEmbeddingNode
from qyver.framework.common.dag.node import Node
from qyver.framework.common.data_types import Vector
from qyver.framework.common.exception import ValidationException
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.common.transform.transform import Step
from qyver.framework.common.transform.transformation_factory import (
    TransformationFactory,
)
from qyver.framework.online.dag.evaluation_result import EvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode
from qyver.framework.online.dag.parent_validator import ParentValidationType


class OnlineCustomVectorEmbeddingNode(
    OnlineNode[CustomVectorEmbeddingNode, Vector], HasLength
):
    def __init__(
        self,
        node: CustomVectorEmbeddingNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(
            node,
            parents,
            storage_manager,
            ParentValidationType.LESS_THAN_TWO_PARENTS,
        )
        self._embedding_transformation = (
            TransformationFactory.create_embedding_transformation(
                self.node.transformation_config
            )
        )

    @property
    @override
    def length(self) -> int:
        return self.node.length

    @property
    def embedding_transformation(self) -> Step[Vector, Vector]:
        return self._embedding_transformation

    @override
    def evaluate_self(
        self,
        parsed_schemas: list[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector]]:
        if self.node.transformation_config.embedding_config.should_return_default(
            context
        ):
            result = EvaluationResult(
                self._get_single_evaluation_result(
                    self.node.transformation_config.embedding_config.default_vector
                )
            )
            return [result] * len(parsed_schemas)
        return [self.evaluate_self_single(schema, context) for schema in parsed_schemas]

    def evaluate_self_single(
        self,
        parsed_schema: ParsedSchema,
        context: ExecutionContext,
    ) -> EvaluationResult[Vector]:
        if len(self.parents) == 0:
            stored_result = self.load_stored_result_or_raise_exception(parsed_schema)
            return EvaluationResult(self._get_single_evaluation_result(stored_result))

        input_: EvaluationResult[list[float]] = cast(
            OnlineNode[Node[Vector], list[float]], self.parents[0]
        ).evaluate_next_single(parsed_schema, context)
        input_value = input_.main.value
        if len(input_value) != self.length:
            raise ValidationException(
                f"{self.class_name} can only process `Vector` inputs"
                + f" of size {self.length}"
                + f", got {len(input_value)}"
            )
        transformed_input_value = self.embedding_transformation.transform(
            Vector(input_value), context
        )
        main = self._get_single_evaluation_result(transformed_input_value)
        return EvaluationResult(main)
