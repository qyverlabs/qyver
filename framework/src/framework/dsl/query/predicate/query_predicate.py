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
from enum import Enum

from beartype.typing import Generic, Sequence, TypeVar
from PIL.Image import Image

from qyver.framework.common.schema.schema_object import SchemaField
from qyver.framework.dsl.query.param import NumericParamType, Param

# Exclude from documentation.
__pdoc__ = {}
__pdoc__["QueryPredicate"] = False

# Operation type
OPT = TypeVar("OPT", bound=Enum)


@dataclass(frozen=True)
class QueryPredicate(Generic[OPT]):
    op: OPT
    params: list[
        SchemaField
        | Param
        | Sequence[str]
        | Sequence[float]
        | Image
        | str
        | int
        | float
        | None
        | tuple[str | None, str | None]
    ]
    weight_param: NumericParamType
