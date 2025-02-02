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

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.recency_node import RecencyNode
from qyver.framework.common.data_types import Vector
from qyver.framework.common.interface.weighted import Weighted
from qyver.framework.query.dag.query_embedding_orphan_node import (
    QueryEmbeddingOrphanNode,
)
from qyver.framework.query.dag.query_evaluation_data_types import (
    QueryEvaluationResult,
)
from qyver.framework.query.dag.query_node import QueryNode
from qyver.framework.query.query_node_input import QueryNodeInput


class QueryRecencyNode(QueryEmbeddingOrphanNode[int, RecencyNode, int]):
    def __init__(self, node: RecencyNode, parents: Sequence[QueryNode]) -> None:
        super().__init__(node, parents, int)

    @override
    def evaluate(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> QueryEvaluationResult[Vector]:
        return super().evaluate(
            self._merge_inputs(
                [
                    inputs,
                    {self.node_id: [QueryNodeInput(Weighted(context.now()), False)]},
                ]
            ),
            context,
        )
