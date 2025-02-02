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

from beartype.typing import Any

from qyver.framework.common.interface.comparison_operation_type import (
    ComparisonOperationType,
)
from qyver.framework.common.storage.field.field_data_type import FieldDataType
from qyver.framework.common.storage.query.vdb_filter import VDBFilter

OR_OPERATOR = "|"
AND_OPERATOR = " "  # it is really a space

NUMBER_OPERATOR_MAP: dict[ComparisonOperationType, str] = {
    ComparisonOperationType.EQUAL: "@%s:[%s %s]",
    ComparisonOperationType.NOT_EQUAL: "(-@%s:[%s %s])",
    ComparisonOperationType.GREATER_THAN: "@%s:[(%s +inf]",
    ComparisonOperationType.LESS_THAN: "@%s:[-inf (%s]",
    ComparisonOperationType.GREATER_EQUAL: "@%s:[%s +inf]",
    ComparisonOperationType.LESS_EQUAL: "@%s:[-inf %s]",
}

TEXT_OPERATOR_MAP: dict[ComparisonOperationType, str] = {
    ComparisonOperationType.EQUAL: '@%s:"%s"',
    ComparisonOperationType.NOT_EQUAL: '-@%s:"%s"',
}

STRING_LIST_OPERATOR_MAP: dict[ComparisonOperationType, str] = {
    ComparisonOperationType.CONTAINS: "@%s:{%s}",
    ComparisonOperationType.NOT_CONTAINS: "-@%s:{%s}",
    ComparisonOperationType.CONTAINS_ALL: "@%s:{%s}",  # splitting it into multiple CONTAINS
}


@dataclass(frozen=True)
class RedisFilter(VDBFilter):
    def get_prefix(self) -> str:
        operator_map = self._get_operator_map()
        if self.op == ComparisonOperationType.IN:
            return self._join_operator(operator_map, ComparisonOperationType.EQUAL, OR_OPERATOR)
        if self.op == ComparisonOperationType.NOT_IN:
            return self._join_operator(operator_map, ComparisonOperationType.NOT_EQUAL, AND_OPERATOR)
        if self.op in [
            ComparisonOperationType.CONTAINS,
            ComparisonOperationType.NOT_CONTAINS,
        ]:
            value_text = f" {OR_OPERATOR} ".join(f'"{value}"' for value in self.field_value.decode("utf-8").split(", "))
            return self._fill_template(operator_map, self.op, value_text)
        if self.op == ComparisonOperationType.CONTAINS_ALL:
            values = [
                self._fill_template(operator_map, self.op, f'"{value}"')
                for value in self.field_value.decode("utf-8").split(", ")
            ]
            value_text = " ".join(values)
            return f"({value_text})"
        if self.op in operator_map:
            return self._fill_template(operator_map, self.op, self.field_value)
        raise NotImplementedError(f"Unsupported comparison operation: {self.op}")

    def _get_operator_map(self) -> dict[ComparisonOperationType, str]:
        if self.field.data_type == FieldDataType.STRING:
            return TEXT_OPERATOR_MAP
        if self.field.data_type in [FieldDataType.INT, FieldDataType.DOUBLE]:
            return NUMBER_OPERATOR_MAP
        if self.field.data_type == FieldDataType.STRING_LIST:
            return STRING_LIST_OPERATOR_MAP
        raise NotImplementedError(f"Unsupported filter field type: {self.field.data_type}")

    def _join_operator(self, operator_map: dict, op: ComparisonOperationType, join_operator: str) -> str:
        value_text = join_operator.join([self._fill_template(operator_map, op, value) for value in self.field_value])
        return f"({value_text})"

    def _fill_template(self, operator_map: dict, op: ComparisonOperationType, value: Any) -> str:
        three_member_ops = [
            ComparisonOperationType.EQUAL,
            ComparisonOperationType.NOT_EQUAL,
        ]
        template_args = (
            (self.field.name, value, value)
            if operator_map == NUMBER_OPERATOR_MAP and op in three_member_ops
            else (self.field.name, value)
        )
        return f"({operator_map[op] % template_args})"
