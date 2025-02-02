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

from beartype.typing import Any
from typing_extensions import override

from qyver.framework.common.dag.node import Node, NodeDataT
from qyver.framework.common.schema.schema_object import SchemaObject
from qyver.framework.common.util.named_function_evaluator import NamedFunction


class NamedFunctionNode(Node[NodeDataT]):
    def __init__(
        self,
        named_function: NamedFunction,
        schema: SchemaObject,
        return_type: type[NodeDataT],
    ) -> None:
        super().__init__(return_type, [], schemas={schema})
        self.named_function = named_function
        self.return_type = return_type

    @override
    def _get_node_id_parameters(self) -> dict[str, Any]:
        return {
            "schemas": self.schemas,
            "named_function": self.named_function,
            "return_type": self.return_type,
        }
