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

from dataclasses import dataclass

from beartype.typing import Generic, Sequence

from qyver.framework.common.schema.id_schema_object import IdSchemaObject
from qyver.framework.common.schema.schema_object import SFT, SchemaField


class ParsedSchemaField(Generic[SFT]):
    def __init__(self, schema_field: SchemaField[SFT], value: SFT) -> None:
        self.schema_field = schema_field
        self.value = value

    @classmethod
    def from_schema_field(cls, schema_field: SchemaField[SFT], value: SFT) -> ParsedSchemaField:
        return cls(schema_field, schema_field.parse(value))

    def __str__(self) -> str:
        return f"{type(self).__name__} of ({self.schema_field})"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class ParsedSchema:
    schema: IdSchemaObject
    id_: str
    fields: Sequence[ParsedSchemaField]


@dataclass
class ParsedSchemaWithEvent(ParsedSchema):
    event_parsed_schema: EventParsedSchema


@dataclass
class EventParsedSchema(ParsedSchema):
    created_at: int
