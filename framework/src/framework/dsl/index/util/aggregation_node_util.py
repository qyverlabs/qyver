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

from qyver.framework.common.dag.aggregation_node import AggregationNode
from qyver.framework.common.dag.effect_modifier import EffectModifier
from qyver.framework.common.dag.embedding_node import EmbeddingNode
from qyver.framework.common.dag.node import Node
from qyver.framework.common.data_types import Vector
from qyver.framework.common.exception import InitializationException
from qyver.framework.common.interface.weighted import Weighted
from qyver.framework.common.space.config.aggregation.aggregation_config import (
    AggregationInputT,
)
from qyver.framework.common.space.config.embedding.embedding_config import (
    EmbeddingInputT,
)
from qyver.framework.dsl.index.util.aggregation_effect_group import (
    AggregationEffectGroup,
)
from qyver.framework.dsl.index.util.event_aggregation_effect_group import (
    EventAggregationEffectGroup,
)
from qyver.framework.dsl.index.util.event_aggregation_node_util import (
    EventAggregationNodeUtil,
)


class AggregationNodeUtil:
    @staticmethod
    def init_aggregation_node(
        aggregation_effect_group: AggregationEffectGroup[AggregationInputT, EmbeddingInputT],
        effect_modifier: EffectModifier,
    ) -> AggregationNode[AggregationInputT, EmbeddingInputT]:
        if len(aggregation_effect_group.effects) == 0:
            raise InitializationException("AggregationNode initialization needs a non-empty set of Effects.")
        event_aggregation_effect_groups = EventAggregationEffectGroup.group_by_event_and_affecting_schema(
            aggregation_effect_group.effects
        )
        eans = [
            EventAggregationNodeUtil.init_event_aggregation_node(eg, effect_modifier)
            for eg in event_aggregation_effect_groups
        ]
        weighted_eans: list[Weighted[Node[Vector]]] = [
            Weighted(parent, effect_modifier.event_influence) for parent in eans
        ]
        affected_node = aggregation_effect_group.space._get_embedding_node(aggregation_effect_group.affected_schema)
        if not isinstance(affected_node, EmbeddingNode):
            raise InitializationException(
                f"AggregationNode affected node of type {type(affected_node).__name__} does not have aggregation set."
            )
        weighted_affected_node: Weighted[Node[Vector]] = Weighted(affected_node, 1 - effect_modifier.event_influence)

        aggregation_node = AggregationNode(
            weighted_eans + [weighted_affected_node],
            {effect.dag_effect for effect in aggregation_effect_group.effects},
            affected_node.transformation_config,
        )
        return aggregation_node
