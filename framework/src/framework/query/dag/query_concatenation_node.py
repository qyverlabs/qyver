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

import math
from functools import reduce

from beartype.typing import Sequence, cast
from typing_extensions import override

from qyver.framework.common.dag.concatenation_node import ConcatenationNode
from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.node import Node
from qyver.framework.common.data_types import NodeDataTypes, Vector
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.interface.weighted import Weighted
from qyver.framework.common.space.config.normalization.normalization_config import (
    ConstantNormConfig,
)
from qyver.framework.common.space.normalization.normalization import (
    ConstantNorm,
    L2Norm,
)
from qyver.framework.query.dag.exception import QueryEvaluationException
from qyver.framework.query.dag.invert_if_addressed_query_node import (
    InvertIfAddressedQueryNode,
)
from qyver.framework.query.dag.query_evaluation_data_types import (
    QueryEvaluationResult,
)
from qyver.framework.query.dag.query_node import QueryNode
from qyver.framework.query.query_node_input import QueryNodeInput


class QueryConcatenationNode(InvertIfAddressedQueryNode[ConcatenationNode, Vector]):
    def __init__(
        self,
        node: ConcatenationNode,
        parents: Sequence[QueryNode[Node[Vector], Vector]],
    ) -> None:
        super().__init__(node, parents)
        self._denormalizer = self._create_denormalizer()
        self._l2_norm = L2Norm()

    def _create_denormalizer(self) -> ConstantNorm:
        return ConstantNorm(self.node.create_normalization_config([1.0] * len(self.node.parents)))

    @override
    def invert_and_readdress(self, node_inputs: Sequence[Weighted[NodeDataTypes]]) -> dict[str, list[QueryNodeInput]]:
        # All of the inputs are vectors having the same dimension as the CN.
        self._validate_inputs_to_be_inverted(node_inputs)
        # Each vector (outer list item) has the same number of
        # parts (inner list items) as the number of parents.
        split_weighted_vectors: list[list[Weighted[Vector]]] = [
            self._split_weighted_vector(cast(Weighted[Vector], node_input)) for node_input in node_inputs
        ]
        return self._address_split_weighted_vectors(split_weighted_vectors)

    def _validate_inputs_to_be_inverted(self, node_inputs: Sequence[Weighted[NodeDataTypes]]) -> None:
        if any(invalid_inputs := [node_input for node_input in node_inputs if not isinstance(node_input.item, Vector)]):
            raise QueryEvaluationException(
                "The inputs that need to be inverted must be " + f"vectors, got {invalid_inputs}"
            )
        if any(
            invalid_inputs_lengths := [
                cast(Vector, node_input.item).dimension
                for node_input in node_inputs
                if cast(Vector, node_input.item).dimension != self.node.length
            ]
        ):
            raise QueryEvaluationException(
                "The inputs that need to be inverted must have the same dimension "
                + f"as the concatenation node, got {invalid_inputs_lengths}"
            )

    def _split_weighted_vector(self, weighted_vector: Weighted[Vector]) -> list[Weighted[Vector]]:
        vector = weighted_vector.item
        parents_without_duplicates = list(dict.fromkeys(self.parents))
        lengths = [cast(HasLength, parent.node).length for parent in parents_without_duplicates]
        vectors = vector.split(lengths)
        return [Weighted(self._denormalizer.denormalize(vector), weighted_vector.weight) for vector in vectors]

    def _address_split_weighted_vectors(
        self, split_weighted_vectors: Sequence[Sequence[Weighted[Vector]]]
    ) -> dict[str, list[QueryNodeInput]]:
        return {
            parent.node_id: [
                QueryNodeInput(weighted_vectors[i], to_invert=True) for weighted_vectors in split_weighted_vectors
            ]
            for i, parent in enumerate(self.parents)
        }

    def _validate_parent_results(self, parent_results: Sequence[QueryEvaluationResult]) -> None:
        super()._validate_parent_results(parent_results)
        if invalid_parent_result_types := {
            type(parent_result.value).__name__
            for parent_result in parent_results
            if not isinstance(parent_result.value, Vector)
        }:
            raise QueryEvaluationException(f"Parent results must be vectors, got {invalid_parent_result_types}")

    @override
    def _evaluate_parent_results(
        self, parent_results: Sequence[QueryEvaluationResult], context: ExecutionContext
    ) -> QueryEvaluationResult[Vector]:
        vectors_with_weights = [
            (
                cast(Vector, result.value),
                context.get_weight_of_node(self.parents[i].node_id),
            )
            for i, result in enumerate(parent_results)
        ]
        weighted_vectors = [vector * weight for vector, weight in vectors_with_weights]
        concatenated_vector = reduce(lambda a, b: a.concatenate(b), weighted_vectors)
        normalized_vector = self._normalize_vector(concatenated_vector, vectors_with_weights)
        return QueryEvaluationResult(self._compansate_vector(normalized_vector, weighted_vectors))

    def _normalize_vector(self, vector: Vector, vectors_with_weights: Sequence[tuple[Vector, float]]) -> Vector:
        norm = ConstantNorm(
            self.node.create_normalization_config(
                [weight for vector, weight in vectors_with_weights if self._l2_norm.norm(vector.value) != 0]
            )
        )
        return norm.normalize(vector)

    def _compansate_vector(self, vector: Vector, weighted_vectors: list[Vector]) -> Vector:
        compensation_factor = self._calculate_compensation_factor(weighted_vectors)
        compensation_factor_norm = ConstantNorm(ConstantNormConfig(compensation_factor))
        return compensation_factor_norm.denormalize(vector)

    def _calculate_compensation_factor(self, weighted_vectors: Sequence[Vector]) -> float:
        num_non_0_spaces = len(
            [weighted_vector for weighted_vector in weighted_vectors if self._l2_norm.norm(weighted_vector.value) != 0]
        )
        if num_non_0_spaces == 0:
            return 1.0
        return math.sqrt(len(self.parents) / num_non_0_spaces)
