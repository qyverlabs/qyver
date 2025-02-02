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

from beartype.typing import Generic

from qyver.framework.common.const import INMEMORY_PUT_CHUNK_SIZE
from qyver.framework.common.observable import Publisher
from qyver.framework.common.parser.data_parser import DataParser
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.schema.id_schema_object import IdSchemaObjectT
from qyver.framework.common.source.source import Source
from qyver.framework.common.source.types import SourceTypeT
from qyver.framework.common.util.collection_util import chunk_list


class InMemorySource(
    Generic[IdSchemaObjectT, SourceTypeT],
    Publisher[ParsedSchema],
    Source[IdSchemaObjectT, SourceTypeT],
):
    def __init__(self, parser: DataParser[IdSchemaObjectT, SourceTypeT]) -> None:
        super().__init__()
        self.parser = parser

    def put(self, data: SourceTypeT) -> None:
        parsed_schemas: list[ParsedSchema] = self.parser.unmarshal(data)
        for batch in chunk_list(
            data=parsed_schemas, chunk_size=INMEMORY_PUT_CHUNK_SIZE
        ):
            self._dispatch(batch)
