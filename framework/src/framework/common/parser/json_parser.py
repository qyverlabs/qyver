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

from beartype.typing import Any, Generic, Sequence, cast

from qyver.framework.common.parser.data_parser import DataParser
from qyver.framework.common.parser.exception import (
    MissingCreatedAtException,
    MissingIdException,
)
from qyver.framework.common.parser.parsed_schema import (
    EventParsedSchema,
    ParsedSchema,
    ParsedSchemaField,
)
from qyver.framework.common.schema.event_schema_object import (
    EventSchemaObject,
    SchemaReference,
)
from qyver.framework.common.schema.id_schema_object import IdSchemaObjectT
from qyver.framework.common.schema.schema_object import SFT, Blob, SchemaField
from qyver.framework.common.util.dot_separated_path_util import (
    DotSeparatedPathUtil,
    ValuedDotSeparatedPath,
)


class JsonParser(Generic[IdSchemaObjectT], DataParser[IdSchemaObjectT, dict[str, Any]]):
    """
    JsonParser gets a `Json` object and using `str` based dot separated path mapping
    it transforms the `Json` to a desired schema.
    """

    def unmarshal(self, data: dict[str, Any] | Sequence[dict[str, Any]]) -> list[ParsedSchema]:
        """
        Parses the given Json into a list of ParsedSchema objects according to the defined schema and mapping.

        Args:
            data (Json): The Json representation of your data.

        Returns:
            list[ParsedSchema]: A list of ParsedSchema objects that will be processed by the spaces.
        """

        if isinstance(data, dict):
            data = [data]
        return [self._unmarshal_single(json_data) for json_data in data]

    def _unmarshal_single(self, json_data: dict[str, Any]) -> EventParsedSchema | ParsedSchema:
        id_ = self.__ensure_id(json_data)
        parsed_fields: list[ParsedSchemaField] = [
            ParsedSchemaField.from_schema_field(field, parsed_value)
            for field, parsed_value in [
                (field, self._parse_schema_field_value(field, json_data)) for field in self._schema.schema_fields
            ]
            if parsed_value is not None
        ]
        if self._is_event_data_parser:
            return EventParsedSchema(
                self._schema,
                id_,
                parsed_fields,
                self.__ensure_created_at(json_data),
            )

        return ParsedSchema(self._schema, id_, parsed_fields)

    def _marshal(
        self,
        parsed_schemas: list[ParsedSchema],
    ) -> list[dict[str, Any]]:
        """
        Converts a ParsedSchema objects back into a list of Json objects.
        You can use this functionality to check, if your mapping was defined properly.

        Args:
            parsed_schemas (list[ParsedSchema]): ParserSchema in a list that you can
                retrieve after unmarshalling your `Json`.

        Returns:
            list[Json]: List of Json representation of the schemas.
        """
        return [
            self.__construct_json(list_of_schema_fields)
            for list_of_schema_fields in [
                self.__get_all_fields_from_parsed_schema(parsed_schema) for parsed_schema in parsed_schemas
            ]
        ]

    def __construct_json(self, parsed_schema_fields: list[ParsedSchemaField]) -> dict[str, Any]:
        altered_parsed_schema_fields = self._handle_parsed_schema_fields(parsed_schema_fields)
        return DotSeparatedPathUtil.to_dict(
            [
                ValuedDotSeparatedPath(
                    self._get_path(field.schema_field),
                    field.value,
                )
                for field in altered_parsed_schema_fields
            ]
        )

    def __ensure_id(self, data: dict[str, Any]) -> str:
        id_ = DotSeparatedPathUtil.get(data, self._id_name)
        if not self._is_id_value_valid(id_):
            raise MissingIdException("The mandatory id field is missing from the input object.")
        return str(id_)

    def __ensure_created_at(self, data: dict[str, Any]) -> int:
        created_at = DotSeparatedPathUtil.get(data, self._created_at_name)
        if not self._is_created_at_value_valid(created_at):
            raise MissingCreatedAtException("The mandatory created_at field is missing from the input object.")
        return cast(int, created_at)

    def _parse_schema_field_value(self, field: SchemaField[SFT], data: dict[str, Any]) -> SFT | None:
        path: str = self._get_path(field)
        parsed_value = DotSeparatedPathUtil.get(data, path)

        if isinstance(field, SchemaReference):
            return cast(SFT, str(parsed_value))

        if isinstance(field, Blob):
            return cast(SFT, self.blob_loader.load(parsed_value))

        return parsed_value

    def __get_all_fields_from_parsed_schema(self, parsed_schema: ParsedSchema) -> list[ParsedSchemaField]:
        return (
            list(parsed_schema.fields)
            + [ParsedSchemaField.from_schema_field(self._schema.id, parsed_schema.id_)]
            + (
                [
                    ParsedSchemaField.from_schema_field(
                        cast(EventSchemaObject, self._schema).created_at,
                        cast(EventParsedSchema, parsed_schema).created_at,
                    )
                ]
                if self._is_event_data_parser
                else []
            )
        )
