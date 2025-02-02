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

from beartype.typing import Sequence
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.data_types import Vector
from qyver.framework.common.space.config.normalization.normalization_config import (
    ConstantNormConfig,
)
from qyver.framework.common.space.normalization.normalization import ConstantNorm
from qyver.framework.common.transform.transform import Step


class AvarageNormalizationStep(Step[list[Vector], Sequence[Vector]]):
    @override
    def transform(
        self,
        input_: list[Vector],
        context: ExecutionContext,
    ) -> list[Vector]:
        normalization = ConstantNorm(ConstantNormConfig(len(input_)))
        return [normalization.normalize(vector) for vector in input_]
