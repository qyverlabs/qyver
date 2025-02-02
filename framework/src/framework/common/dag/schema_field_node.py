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

from qyver.framework.common.dag.dag_effect import DagEffect
from qyver.framework.common.dag.node import Node
from qyver.framework.common.schema.schema_object import SFT, SchemaField


class SchemaFieldNode(Generic[SFT], Node[SFT]):
    def __init__(self, schema_field: SchemaField[SFT], dag_effects: set[DagEffect] | None = None) -> None:
        super().__init__(
            schema_field.type_,
            [],
            schemas={schema_field.schema_obj},
            dag_effects=dag_effects,
        )
        self.schema_field = schema_field

    @override
    def _get_node_id_parameters(self) -> dict[str, Any]:
        return {
            "schema_field": self.schema_field,
            "schemas": self.schemas,
            "dag_effects": self.dag_effects,
        }
