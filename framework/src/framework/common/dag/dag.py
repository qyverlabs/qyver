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

from beartype.typing import Sequence

from qyver.framework.common.dag.dag_effect import DagEffect
from qyver.framework.common.dag.exception import InvalidDagException
from qyver.framework.common.dag.index_node import IndexNode
from qyver.framework.common.dag.node import Node
from qyver.framework.common.dag.schema_dag import SchemaDag
from qyver.framework.common.exception import (
    DuplicateNodeIdException,
    InvalidDagEffectException,
    InvalidSchemaException,
)
from qyver.framework.common.schema.schema_object import SchemaObject


class Dag:
    def __init__(self, nodes: list[Node], dag_effects: set[DagEffect] | None = None) -> None:
        self.nodes = nodes
        self._index_node = self.__init_index_node(self.nodes)
        self.__check_for_node_id_duplication()
        self.dag_effects = dag_effects or set()
        node_id_schema_map: dict[str, set[SchemaObject]] = self.__init_node_id_schema_map(self.nodes)
        node_id_dag_effect_map: dict[str, set[DagEffect]] = self.__init_node_id_dag_effect_map(self.nodes)
        self.__schemas: set[SchemaObject] = self.__init_schemas(node_id_schema_map)
        self.__schema_dag_map: dict[SchemaObject, SchemaDag] = self.__init_schema_schema_dag_map(
            self.__schemas, node_id_schema_map
        )
        self.__dag_effect_dag_map: dict[DagEffect, SchemaDag] = self.__init_dag_effect_schema_dag_map(
            self.dag_effects, node_id_dag_effect_map
        )

    @property
    def schemas(self) -> set[SchemaObject]:
        return self.__schemas

    @property
    def index_node(self) -> IndexNode:
        return self._index_node

    def project_to_schema(self, schema: SchemaObject) -> SchemaDag:
        if (dag := self.__schema_dag_map.get(schema)) is not None:
            return dag
        raise InvalidSchemaException(f"SchemaDag for the given schema ({schema._base_class_name}) doesn't exist.")

    def project_to_dag_effect(self, dag_effect: DagEffect) -> SchemaDag:
        if (dag := self.__dag_effect_dag_map.get(dag_effect)) is not None:
            return dag
        raise InvalidDagEffectException(
            f"SchemaDag for the given dag effect ({dag_effect} "
            + f"- {dag_effect.event_schema._base_class_name}) doesn't exist."
        )

    def __init_index_node(self, nodes: Sequence[Node]) -> IndexNode:
        if index_node := next((node for node in nodes if isinstance(node, IndexNode)), None):
            return index_node
        raise InvalidDagException("Dag doesn't have an IndexNode.")

    def __init_node_id_schema_map(self, nodes: list[Node]) -> dict[str, set[SchemaObject]]:
        return {node.node_id: node.schemas for node in nodes}

    def __init_node_id_dag_effect_map(self, nodes: list[Node]) -> dict[str, set[DagEffect]]:
        return {node.node_id: node.dag_effects for node in nodes}

    def __init_schemas(self, node_id_schema_map: dict[str, set[SchemaObject]]) -> set[SchemaObject]:
        return {schema for schemas in node_id_schema_map.values() for schema in schemas}

    def __init_schema_schema_dag_map(
        self,
        schemas: set[SchemaObject],
        node_id_schema_map: dict[str, set[SchemaObject]],
    ) -> dict[SchemaObject, SchemaDag]:
        return {schema: self.__project_to_schema(schema, node_id_schema_map) for schema in schemas}

    def __project_to_schema(self, schema: SchemaObject, node_id_schema_map: dict[str, set[SchemaObject]]) -> SchemaDag:
        filtered_nodes = {node for node in self.nodes if schema in node_id_schema_map[node.node_id]}
        projected_parents = set(parent for node in filtered_nodes for parent in node.project_parents_to_schema(schema))
        return SchemaDag(
            schema,
            list(projected_parents.union(filtered_nodes)),
        )

    def __init_dag_effect_schema_dag_map(
        self,
        dag_effects: set[DagEffect],
        node_id_dag_effect_map: dict[str, set[DagEffect]],
    ) -> dict[DagEffect, SchemaDag]:
        return {
            dag_effect: self.__project_to_dag_effect(dag_effect, node_id_dag_effect_map) for dag_effect in dag_effects
        }

    def __project_to_dag_effect(
        self, dag_effect: DagEffect, node_id_dag_effect_map: dict[str, set[DagEffect]]
    ) -> SchemaDag:
        filtered_nodes = {node for node in self.nodes if dag_effect in node_id_dag_effect_map[node.node_id]}
        projected_parents = set(
            parent for node in filtered_nodes for parent in node.project_parents_for_dag_effect(dag_effect)
        )
        return SchemaDag(
            dag_effect.event_schema,
            list(projected_parents.union(filtered_nodes)),
        )

    def __check_for_node_id_duplication(self) -> None:
        node_ids = set()
        for node in self.nodes:
            if node.node_id in node_ids:
                raise DuplicateNodeIdException(f"Node id: {node} is duplicated!")
            node_ids.add(node._node_id)
