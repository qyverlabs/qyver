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

from beartype.typing import Generic, Mapping, Sequence
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.embedding_node import EmbeddingNodeT
from qyver.framework.common.dag.node import NodeDataT
from qyver.framework.common.space.config.aggregation.aggregation_config import (
    AggregationInputT,
)
from qyver.framework.query.dag.query_embedding_node import QueryEmbeddingNode
from qyver.framework.query.dag.query_evaluation_data_types import (
    QueryEvaluationResult,
)
from qyver.framework.query.query_node_input import QueryNodeInput


class QueryEmbeddingOrphanNode(
    QueryEmbeddingNode[AggregationInputT, EmbeddingNodeT, NodeDataT],
    Generic[AggregationInputT, EmbeddingNodeT, NodeDataT],
):
    @override
    def _evaluate_parents(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> list[QueryEvaluationResult]:
        return []
