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

from beartype.typing import cast

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.dag_effect import DagEffect
from qyver.framework.common.exception import InvalidDagEffectException
from qyver.framework.common.observable import Subscriber
from qyver.framework.common.parser.parsed_schema import (
    EventParsedSchema,
    ParsedSchema,
    ParsedSchemaWithEvent,
)
from qyver.framework.common.storage_manager.storage_manager import StorageManager
from qyver.framework.dsl.index.index import Index
from qyver.framework.evaluator.online_dag_evaluator import OnlineDagEvaluator


class InMemoryDataProcessor(Subscriber[ParsedSchema]):
    MAX_SAVE_DEPTH = 10

    def __init__(
        self,
        evaluator: OnlineDagEvaluator,
        storage_manager: StorageManager,
        context: ExecutionContext,
        index: Index,
    ) -> None:
        super().__init__()
        self.evaluator = evaluator
        self.context = context
        self.storage_manager = storage_manager
        self.effect_schemas = set(index._effect_schemas)
        self._schema_type_schema_mapper = index._schema_type_schema_mapper
        self._dag_effects = index._dag_effects

    def update(self, messages: list[ParsedSchema]) -> None:
        regular_msgs: list[ParsedSchema] = []
        for message in messages:
            if message.schema in self.effect_schemas:
                self._process_event(cast(EventParsedSchema, message))
            else:
                regular_msgs.append(message)
        if regular_msgs:
            for parsed_schema in regular_msgs:
                self.storage_manager.write_parsed_schema_fields(
                    parsed_schema.id_, parsed_schema.fields
                )
            self.evaluator.evaluate(regular_msgs, self.context)

    def _process_event(
        self,
        event_parsed_schema: EventParsedSchema,
    ) -> None:
        effect_parsed_schema_map = self._map_event_parsed_schema_by_dag_effects(
            event_parsed_schema
        )
        for effect, parsed_schema_with_event in effect_parsed_schema_map.items():
            self.evaluator.evaluate_by_dag_effect(
                parsed_schema_with_event, self.context, effect
            )

    def _map_event_parsed_schema_by_dag_effects(
        self, event_parsed_schema: EventParsedSchema
    ) -> dict[DagEffect, ParsedSchemaWithEvent]:
        active_effects = [
            effect
            for effect in self._dag_effects
            if effect.event_schema == event_parsed_schema.schema
        ]
        effect_parsed_schema_map = dict[DagEffect, ParsedSchemaWithEvent]()
        for effect in active_effects:
            affected_schema_ids = [
                reference.value
                for reference in event_parsed_schema.fields
                if reference.schema_field
                == effect.resolved_affected_schema_reference.reference_field
                and reference.value is not None
            ]
            if len(affected_schema_ids) > 1:
                raise InvalidDagEffectException(f"DagEffect: {effect}")
            if affected_schema_ids:
                effect_parsed_schema_map[effect] = ParsedSchemaWithEvent(
                    effect.resolved_affected_schema_reference.schema,
                    affected_schema_ids[0],
                    [],
                    event_parsed_schema,
                )
        return effect_parsed_schema_map
