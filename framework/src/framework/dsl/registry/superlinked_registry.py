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

from qyver.framework.dsl.executor.executor import Executor
from qyver.framework.dsl.registry.exception import DuplicateElementException


class qyverRegistry:
    __executors: set[Executor] = set()

    @staticmethod
    def register(*items: Executor) -> None:
        for item in items:
            qyverRegistry.__check_for_duplicates(item)
            qyverRegistry.__executors.add(item)

    @staticmethod
    def __check_for_duplicates(item: Executor) -> None:
        if item in qyverRegistry.__executors:
            raise DuplicateElementException(f"{item} already registered!")

    @staticmethod
    def get_executors() -> frozenset[Executor]:
        return frozenset(qyverRegistry.__executors)
