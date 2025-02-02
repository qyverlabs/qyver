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

from abc import ABC, abstractmethod

from beartype.typing import Generic, Mapping, Sequence

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.node import NT
from qyver.framework.query.dag.query_evaluation_data_types import (
    QueryEvaluationResult,
    QueryEvaluationResultT,
)
from qyver.framework.query.query_node_input import QueryNodeInput


class QueryNode(ABC, Generic[NT, QueryEvaluationResultT]):
    def __init__(self, node: NT, parents: Sequence[QueryNode]) -> None:
        super().__init__()
        self._node = node
        self.parents = parents

    @property
    def node(self) -> NT:
        return self._node

    @property
    def node_id(self) -> str:
        return self.node.node_id

    def evaluate_with_validation(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> QueryEvaluationResult[QueryEvaluationResultT]:
        self._validate_evaluation_inputs(inputs)
        return self.evaluate(inputs, context)

    @abstractmethod
    def evaluate(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> QueryEvaluationResult[QueryEvaluationResultT]:
        pass

    def _validate_evaluation_inputs(self, inputs: Mapping[str, Sequence[QueryNodeInput]]) -> None:
        pass

    def _merge_inputs(
        self,
        inputs: Sequence[Mapping[str, Sequence[QueryNodeInput]]],
    ) -> dict[str, Sequence[QueryNodeInput]]:
        if not inputs:
            return {}
        merged_inputs_dict = dict(inputs[0])
        for inputs_item in inputs[1:]:
            for node_id, input_ in inputs_item.items():
                node_inputs = list(merged_inputs_dict.get(node_id, [])) + list(input_)
                merged_inputs_dict.update({node_id: node_inputs})
        return merged_inputs_dict
