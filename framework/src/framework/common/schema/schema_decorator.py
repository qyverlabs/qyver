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

import inspect

from beartype.typing import Any, Sequence, TypeAlias, cast

from qyver.framework.common.schema.event_schema_object import (
    CreatedAtField,
    EventSchemaObject,
)
from qyver.framework.common.schema.general_type import T
from qyver.framework.common.schema.id_schema_object import IdField, IdSchemaObject
from qyver.framework.common.schema.schema_object import (
    SchemaField,
    SchemaFieldDescriptor,
)
from qyver.framework.common.schema.schema_type import SchemaType
from qyver.framework.common.schema.schema_validator import SchemaValidator

DEFAULT_ID_FIELD_NAME = "id"
DEFAULT_CREATED_AT_FIELD_NAME = "created_at"


class SchemaDecorator:
    @staticmethod
    def decorate(
        schema_cls: type[T],
        schema_type: SchemaType,
        schema_name: str,
        schema_field_descriptors: list[SchemaFieldDescriptor],
        schema_validator: SchemaValidator,
    ) -> Any:
        return SchemaDecorator.__get_decorated(
            schema_cls,
            schema_name,
            schema_field_descriptors,
            IdSchemaObject if schema_type == SchemaType.SCHEMA else EventSchemaObject,
            schema_validator,
        )

    @staticmethod
    def __get_decorated(
        schema_cls: type[T],
        schema_name: str,
        schema_field_descriptors: list[SchemaFieldDescriptor],
        base_class: TypeAlias,
        schema_validator: SchemaValidator,
    ) -> Any:
        schema_validator.validate_id_field(schema_cls)
        id_field_name = SchemaDecorator.__get_field_name(schema_cls, IdField)
        if base_class is EventSchemaObject:
            schema_validator.validate_created_at_field(schema_cls)
            created_at_field_name: str = SchemaDecorator.__get_field_name(
                schema_cls, CreatedAtField
            )

        class Decorated(base_class):
            def __init__(self) -> None:
                if base_class is EventSchemaObject:
                    super().__init__(
                        schema_cls,
                        schema_name,
                        id_field_name,
                        created_at_field_name,
                    )
                else:
                    super().__init__(schema_cls, schema_name, id_field_name)

                self._schema_fields = [
                    self._init_field(schema_field_descriptor)
                    for schema_field_descriptor in schema_field_descriptors
                ]

            def _get_schema_fields(self) -> Sequence[SchemaField]:
                """Returns all declared SchemaFields. Does not include the mandatory "id" field."""
                return self._schema_fields

        return cast(
            type[Decorated],
            type("DecoratedType", (Decorated, schema_cls), {}),
        )

    @staticmethod
    def __get_field_name(schema_cls: type[T], field_type: type) -> str:
        return next(
            name
            for name, type_ in schema_cls.__annotations__.items()
            if inspect.isclass(type_) and issubclass(type_, field_type)
        )
