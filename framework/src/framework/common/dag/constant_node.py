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

from beartype.typing import Any, Generic
from typing_extensions import override

from qyver.framework.common.dag.node import Node, NodeDataT
from qyver.framework.common.schema.schema_object import SchemaObject


class ConstantNode(Generic[NodeDataT], Node[NodeDataT]):
    def __init__(self, value: NodeDataT, schema: SchemaObject) -> None:
        super().__init__(type(value), [], schemas={schema})
        self.value = value

    @override
    def _get_node_id_parameters(self) -> dict[str, Any]:
        return {"schemas": self.schemas, "value": str(self.value)}
