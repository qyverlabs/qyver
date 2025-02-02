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

from enum import Enum


class FieldDataType(Enum):
    BLOB = "BLOB"
    DOUBLE = "DOUBLE"
    FLOAT_LIST = "FLOAT_LIST"
    IMAGE_DATA = "IMAGE_DATA"
    INT = "INT"
    JSON = "JSON"
    STRING = "STRING"
    STRING_LIST = "STRING_LIST"
    VECTOR = "VECTOR"
