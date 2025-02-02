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

from qyver.framework.common.dag.comparison_filter_node import ComparisonFilterNode
from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.online.dag.default_online_node import DefaultOnlineNode
from qyver.framework.online.dag.evaluation_result import SingleEvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode
from qyver.framework.online.dag.parent_validator import ParentValidationType


class OnlineComparisonFilterNode(DefaultOnlineNode[ComparisonFilterNode, bool]):
    def __init__(
        self,
        node: ComparisonFilterNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(
            node,
            parents,
            storage_manager,
            ParentValidationType.EXACTLY_ONE_PARENT,
        )

    @override
    def _evaluate_singles(
        self,
        parent_results: Sequence[dict[OnlineNode, SingleEvaluationResult]],
        context: ExecutionContext,
    ) -> Sequence[bool | None]:
        return [self._evaluate_single(parent_result) for parent_result in parent_results]

    def _evaluate_single(
        self,
        parent_results: dict[OnlineNode, SingleEvaluationResult],
    ) -> bool:
        parent_result: SingleEvaluationResult = list(parent_results.values())[0]
        return self.node.comparison_operation.evaluate(parent_result.value)
