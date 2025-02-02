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

from qyver.framework.compiler.compiled_node_registry import CompiledNodeRegistry
from qyver.framework.online.dag.online_aggregation_node import (
    OnlineAggregationNode,
)
from qyver.framework.online.dag.online_categorical_similarity_node import (
    OnlineCategoricalSimilarityNode,
)
from qyver.framework.online.dag.online_chunking_node import OnlineChunkingNode
from qyver.framework.online.dag.online_comparison_filter_node import (
    OnlineComparisonFilterNode,
)
from qyver.framework.online.dag.online_concatenation_node import (
    OnlineConcatenationNode,
)
from qyver.framework.online.dag.online_constant_node import OnlineConstantNode
from qyver.framework.online.dag.online_custom_vector_embedding_node import (
    OnlineCustomVectorEmbeddingNode,
)
from qyver.framework.online.dag.online_event_aggregation_node import (
    OnlineEventAggregationNode,
)
from qyver.framework.online.dag.online_image_embedding_node import (
    OnlineImageEmbeddingNode,
)
from qyver.framework.online.dag.online_index_node import OnlineIndexNode
from qyver.framework.online.dag.online_named_function_node import (
    OnlineNamedFunctionNode,
)
from qyver.framework.online.dag.online_node import OnlineNode
from qyver.framework.online.dag.online_number_embedding_node import (
    OnlineNumberEmbeddingNode,
)
from qyver.framework.online.dag.online_recency_node import OnlineRecencyNode
from qyver.framework.online.dag.online_schema_field_node import (
    OnlineSchemaFieldNode,
)
from qyver.framework.online.dag.online_text_embedding_node import (
    OnlineTextEmbeddingNode,
)

DEFAULT_NODE_TYPES: list[type[OnlineNode]] = [
    OnlineAggregationNode,
    OnlineChunkingNode,
    OnlineCategoricalSimilarityNode,
    OnlineComparisonFilterNode,
    OnlineConcatenationNode,
    OnlineConstantNode,
    OnlineCustomVectorEmbeddingNode,
    OnlineEventAggregationNode,
    OnlineImageEmbeddingNode,
    OnlineIndexNode,
    OnlineNamedFunctionNode,
    OnlineNumberEmbeddingNode,
    OnlineRecencyNode,
    OnlineSchemaFieldNode,
    OnlineTextEmbeddingNode,
    # * Add new OnlineNode implementations here
]


class OnlineNodeRegistry(CompiledNodeRegistry[OnlineNode]):
    def __init__(self) -> None:
        # This type ignore is a python "bug", we cannot pass an abstract class
        # when it's type-hinted as type.
        super().__init__(OnlineNode, DEFAULT_NODE_TYPES)  # type: ignore
