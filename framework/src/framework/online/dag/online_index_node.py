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
from qyver.framework.common.dag.exception import ParentCountException
from qyver.framework.common.dag.index_node import IndexNode
from qyver.framework.common.dag.node import Node
from qyver.framework.common.data_types import Vector
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.schema.schema_object import SchemaObject
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.online.dag.evaluation_result import EvaluationResult
from qyver.framework.online.dag.online_node import OnlineNode


class OnlineIndexNode(OnlineNode[IndexNode, Vector], HasLength):
    def __init__(
        self,
        node: IndexNode,
        parents: Sequence[OnlineNode[Node[Vector], Vector]],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(node, parents, storage_manager)

    @property
    def length(self) -> int:
        return self.node.length

    def get_parent_for_schema(self, schema: SchemaObject) -> OnlineNode:
        active_parents = [parent for parent in self.parents if schema in cast(Node, parent.node).schemas]
        if len(active_parents) != 1:
            raise ParentCountException(
                f"{self.class_name} must have exactly 1 parent per schema, got {len(active_parents)}"
            )
        return active_parents[0]

    def __get_parent_for_parsed_schemas(self, parsed_schemas: Sequence[ParsedSchema]) -> OnlineNode:
        active_parents = set(self.get_parent_for_schema(parsed_schema.schema) for parsed_schema in parsed_schemas)
        if len(active_parents) != 1:
            raise ParentCountException(
                f"{self.class_name} must have exactly 1 parent per schema, got {len(active_parents)}"
            )
        return cast(OnlineNode[Node[Vector], Vector], next(iter(active_parents)))

    @override
    def evaluate_self(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector] | None]:
        parent: OnlineNode = self.__get_parent_for_parsed_schemas(parsed_schemas)
        parent_results = cast(list[EvaluationResult], self.evaluate_parent(parent, parsed_schemas, context))
        return [
            EvaluationResult(
                self._get_single_evaluation_result(parent_result.main.value),
                [self._get_single_evaluation_result(chunk_result.value) for chunk_result in parent_result.chunks],
            )
            for parent_result in parent_results
        ]
