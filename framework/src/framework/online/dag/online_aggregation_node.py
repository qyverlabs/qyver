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

from beartype.typing import Sequence, cast
from typing_extensions import override

from qyver.framework.common.dag.aggregation_node import AggregationNode
from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.exception import ParentCountException
from qyver.framework.common.data_types import Vector
from qyver.framework.common.exception import (
    MismatchingDimensionException,
    ValidationException,
)
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.interface.weighted import Weighted
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.common.transform.transformation_factory import (
    TransformationFactory,
)
from qyver.framework.online.dag.default_online_node import DefaultOnlineNode
from qyver.framework.online.dag.evaluation_result import SingleEvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode
from qyver.framework.online.dag.parent_validator import ParentValidationType


class OnlineAggregationNode(DefaultOnlineNode[AggregationNode, Vector], HasLength):
    def __init__(
        self,
        node: AggregationNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(
            node,
            parents,
            storage_manager,
            ParentValidationType.AT_LEAST_ONE_PARENT,
        )
        OnlineAggregationNode._validate_parents(parents)
        self._aggregation_transformation = TransformationFactory.create_aggregation_transformation(
            self.node.transformation_config,
        )

    @property
    def length(self) -> int:
        return self.node.length

    @classmethod
    def _validate_parents(cls, parents: list[OnlineNode]) -> None:
        length = cast(HasLength, parents[0]).length
        if any(parent for parent in parents if cast(HasLength, parent).length != length):
            raise ValidationException(f"{cls.__name__} must have parents with the same length.")

    @override
    def _evaluate_singles(
        self,
        parent_results: Sequence[dict[OnlineNode, SingleEvaluationResult]],
        context: ExecutionContext,
    ) -> Sequence[Vector | None]:
        return [self._evaluate_single(parent_result, context) for parent_result in parent_results]

    def _evaluate_single(
        self,
        parent_results: dict[OnlineNode, SingleEvaluationResult],
        context: ExecutionContext,
    ) -> Vector:
        self._check_evaluation_inputs(parent_results)
        not_empty_weighted_vectors = self._get_not_empty_weighted_vectors(list(parent_results.values()))
        if self._no_event_present(not_empty_weighted_vectors):
            return not_empty_weighted_vectors[0].item
        return self._aggregation_transformation.transform(
            not_empty_weighted_vectors,
            context,
        )

    def _check_evaluation_inputs(
        self,
        parent_results: dict[OnlineNode, SingleEvaluationResult],
    ) -> None:
        invalid_type_result_types = [
            result.__class__.__name__ for _, result in parent_results.items() if not isinstance(result.value, Vector)
        ]
        if any(invalid_type_result_types):
            raise ValidationException(
                f"{self.class_name} can only process `Vector` inputs" + f", got {invalid_type_result_types}"
            )
        filtered_parent_results: dict[OnlineNode, SingleEvaluationResult[Vector]] = {
            parent: result for parent, result in parent_results.items() if not cast(Vector, result.value).is_empty
        }
        if not any(filtered_parent_results.items()):
            raise ParentCountException(f"{self.class_name} must have at least 1 parent with valid input.")
        invalid_length_results = [
            result for _, result in filtered_parent_results.items() if result.value.dimension != self.length
        ]
        if any(invalid_length_results):
            raise MismatchingDimensionException(
                f"{self.class_name} can only process inputs having same length"
                + f", got {invalid_length_results[0].value.dimension}"
            )

    def _get_not_empty_weighted_vectors(
        self, parent_result_values: Sequence[SingleEvaluationResult]
    ) -> list[Weighted[Vector]]:
        return [
            Weighted(parent_result.value, weighted_parent.weight)
            for parent_result, weighted_parent in zip(parent_result_values, self.node.weighted_parents)
            if parent_result.value and not cast(Vector, parent_result.value).is_empty
        ]

    def _no_event_present(self, weighted_vectors: Sequence[Weighted[Vector]]) -> bool:
        return len(weighted_vectors) == 1
