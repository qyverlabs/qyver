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

from beartype.typing import Mapping, Sequence
from typing_extensions import override

from qyver.framework.common.dag.custom_node import CustomVectorEmbeddingNode
from qyver.framework.common.data_types import Vector
from qyver.framework.common.interface.weighted import Weighted
from qyver.framework.query.dag.query_embedding_orphan_node import (
    QueryEmbeddingOrphanNode,
)
from qyver.framework.query.dag.query_node import QueryNode
from qyver.framework.query.query_node_input import QueryNodeInput


class QueryCustomVectorEmbeddingNode(QueryEmbeddingOrphanNode[Vector, CustomVectorEmbeddingNode, Vector]):
    def __init__(self, node: CustomVectorEmbeddingNode, parents: Sequence[QueryNode]) -> None:
        super().__init__(node, parents, Vector)

    @override
    def _pre_process_node_inputs(self, inputs: Mapping[str, Sequence[QueryNodeInput]]) -> Sequence[QueryNodeInput]:
        return [self._pre_process_node_input(input_) for input_ in inputs.get(self.node_id) or []]

    def _pre_process_node_input(self, node_input: QueryNodeInput) -> QueryNodeInput:
        result: QueryNodeInput[Vector]
        if isinstance(node_input.value.item, Vector):
            result = node_input
        elif isinstance(node_input.value.item, list):
            result = QueryNodeInput(
                Weighted(Vector(node_input.value.item), node_input.value.weight),
                node_input.to_invert,
            )
        else:
            raise ValueError(
                f"{type(self).__name__} can only evaluate "
                + f"{type(Vector).__name__} and list of floats "
                + f"input, got {type(node_input.value.item).__name__}"
            )
        self.__validate_pre_processed(result)
        return result

    def __validate_pre_processed(self, input_: QueryNodeInput[Vector]) -> None:
        if input_.value.item.dimension != self.node.length:
            raise ValueError(
                f"Wrong dimension of input, expected {self.node.length}, " + f"got {input_.value.item.dimension}"
            )
