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


import hashlib
from dataclasses import asdict

from beartype.typing import Any, Generic, Sequence, TypeVar
from typing_extensions import override

from qyver.framework.common.dag.node import Node, NodeDataT
from qyver.framework.common.data_types import Vector
from qyver.framework.common.schema.schema_object import SchemaField, SchemaObject
from qyver.framework.common.space.config.aggregation.aggregation_config import (
    AggregationInputT,
)
from qyver.framework.common.space.config.transformation_config import (
    TransformationConfig,
)
from qyver.framework.common.space.interface.has_transformation_config import (
    HasTransformationConfig,
)


class EmbeddingNode(
    Generic[AggregationInputT, NodeDataT],
    Node[Vector],
    HasTransformationConfig[AggregationInputT, NodeDataT],
):
    def __init__(
        self,
        parents: Sequence[Node | None],
        transformation_config: TransformationConfig[AggregationInputT, NodeDataT],
        fields_for_identification: set[SchemaField],
        schema: SchemaObject | None = None,
    ) -> None:
        super().__init__(
            Vector,
            [parent for parent in parents if parent is not None],
            {schema} if schema else None,
        )
        self._identifier = self._calculate_node_id_identifier(fields_for_identification)
        self._transformation_config = transformation_config

    @property
    @override
    def length(self) -> int:
        return self._transformation_config.length

    @property
    @override
    def transformation_config(
        self,
    ) -> TransformationConfig[AggregationInputT, NodeDataT]:
        return self._transformation_config

    def _calculate_node_id_identifier(self, fields: set[SchemaField]) -> str:
        """
        This method ensures unique node ID generation by creating a hash of concatenated field names
        when multiple fields exist. This prevents ID collisions between different spaces that may
        share some of the same fields and have the same configuration.
        """
        if len(fields) <= 1:
            return ""
        field_names_text = str(sorted([field.name for field in fields]))
        return hashlib.md5(field_names_text.encode()).hexdigest()[:8]

    @override
    def _get_node_id_parameters(self) -> dict[str, Any]:
        return {
            "transformation_config": asdict(self.transformation_config),
            "identifier": self._identifier,
        }


EmbeddingNodeT = TypeVar("EmbeddingNodeT", bound=EmbeddingNode)
