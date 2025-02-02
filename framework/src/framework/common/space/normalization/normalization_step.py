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

from abc import ABC

from beartype.typing import Sequence
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.data_types import Vector
from qyver.framework.common.space.normalization.normalization import Normalization
from qyver.framework.common.transform.transform import Step


class NormalizationStep(Step[Vector, Vector], ABC):
    def __init__(self, normalization: Normalization, denormalize: bool = False) -> None:
        super().__init__()
        self._normalization = normalization
        self._denormalize = denormalize

    @override
    def transform(
        self,
        input_: Vector,
        context: ExecutionContext,
    ) -> Vector:
        if self._denormalize:
            return self._normalization.denormalize(input_)
        return self._normalization.normalize(input_)


class MultiNormalizationStep(Step[Sequence[Vector], list[Vector]], ABC):
    def __init__(self, normalization: Normalization, denormalize: bool = False) -> None:
        super().__init__()
        self._normalization = normalization
        self._denormalize = denormalize

    @override
    def transform(
        self,
        input_: Sequence[Vector],
        context: ExecutionContext,
    ) -> list[Vector]:
        if self._denormalize:
            return self._normalization.denormalize_multiple(input_)
        return self._normalization.normalize_multiple(input_)
