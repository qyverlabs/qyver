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

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.named_function_node import NamedFunctionNode
from qyver.framework.common.dag.node import NodeDataT
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.common.util.named_function_evaluator import (
    NamedFunctionEvaluator,
)
from qyver.framework.online.dag.evaluation_result import EvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode
from qyver.framework.online.dag.parent_validator import ParentValidationType


class OnlineNamedFunctionNode(OnlineNode[NamedFunctionNode[NodeDataT], NodeDataT]):
    def __init__(
        self,
        node: NamedFunctionNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(
            node,
            parents,
            storage_manager,
            ParentValidationType.NO_PARENTS,
        )

    @override
    def evaluate_self(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[NodeDataT] | None]:
        result = EvaluationResult(self._get_single_evaluation_result(self._evaluate_single(context)))
        return [result] * len(parsed_schemas)

    def _evaluate_single(
        self,
        context: ExecutionContext,
    ) -> NodeDataT:
        result = cast(
            NodeDataT,
            NamedFunctionEvaluator().evaluate(self.node.named_function, context),
        )
        return result
