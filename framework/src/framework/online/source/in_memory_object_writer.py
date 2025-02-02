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

from qyver.framework.common.observable import Subscriber
from qyver.framework.common.parser.json_parser import JsonParser
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.common.storage_manager.storage_manager import StorageManager


class InMemoryObjectWriter(Subscriber[ParsedSchema]):
    def __init__(self, storage_manager: StorageManager) -> None:
        super().__init__()
        self.__storage_manager = storage_manager

    def update(self, messages: list[ParsedSchema]) -> None:
        for message in messages:
            parser = JsonParser(message.schema)
            data = parser.marshal(message)
            for data_element in data:
                self.__storage_manager.write_object_blob(
                    message.schema, message.id_, data_element
                )
