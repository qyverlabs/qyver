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

from beartype.typing import Any
from typing_extensions import override

from qyver.framework.common.data_types import Vector
from qyver.framework.common.schema.blob_information import BlobInformation
from qyver.framework.dsl.query.query_result_converter.query_result_converter import (
    QueryResultConverter,
)


class DefaultQueryResultConverter(QueryResultConverter):
    @override
    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, BlobInformation):
            return value.data or value.path
        if isinstance(value, Vector):
            return value.value.astype(float).tolist()
        return value
