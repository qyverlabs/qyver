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

from dataclasses import dataclass

from qyver.framework.common.schema.event_schema_object import SchemaReference
from qyver.framework.common.schema.id_schema_object import IdSchemaObject


@dataclass(frozen=True)
class ResolvedSchemaReference:
    schema: IdSchemaObject
    reference_field: SchemaReference
    multiplier: float

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(schema={self.schema}, multiplier={self.multiplier}, "
            f"reference_field={self.reference_field})"
        )
