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

from beartype.typing import Generic, Mapping, Sequence, cast
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.named_function_node import NamedFunctionNode
from qyver.framework.common.dag.node import NodeDataT
from qyver.framework.common.util.named_function_evaluator import (
    NamedFunctionEvaluator,
)
from qyver.framework.query.dag.query_evaluation_data_types import (
    QueryEvaluationResult,
)
from qyver.framework.query.dag.query_node import QueryNode
from qyver.framework.query.query_node_input import QueryNodeInput


class QueryNamedFunctionNode(QueryNode[NamedFunctionNode[NodeDataT], NodeDataT], Generic[NodeDataT]):
    def __init__(self, node: NamedFunctionNode[NodeDataT], parents: Sequence[QueryNode]) -> None:
        super().__init__(node, parents)

    @override
    def evaluate(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> QueryEvaluationResult[NodeDataT]:
        return QueryEvaluationResult(
            cast(
                NodeDataT,
                NamedFunctionEvaluator().evaluate(self.node.named_function, context),
            )
        )
