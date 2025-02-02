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

from beartype.typing import Any, Sequence, cast
from redis.commands.search.query import Query

from qyver.framework.common.interface.comparison_operand import (
    ComparisonOperand,
    ComparisonOperation,
)
from qyver.framework.common.interface.comparison_operation_type import (
    ITERABLE_COMPARISON_OPERATION_TYPES,
    LIST_TYPE_COMPATIBLE_TYPES,
)
from qyver.framework.common.storage.field.field import Field
from qyver.framework.common.storage.field.field_data import (
    FieldData,
    VectorFieldData,
)
from qyver.framework.common.storage.query.vdb_knn_search_params import (
    VDBKNNSearchParams,
)
from qyver.framework.common.util.type_validator import TypeValidator
from qyver.framework.storage.redis.query.redis_filter import RedisFilter
from qyver.framework.storage.redis.redis_field_encoder import (
    RedisEncodedTypes,
    RedisFieldEncoder,
)

RANGE_DISTANCE_PARAM_NAME = "__range_dist"
VECTOR_DISTANCE_ALIAS = "__vector_distance"


@dataclass
class RedisQuery:
    query: Query
    query_params: dict[str, Any]


class RedisQueryBuilder:
    def __init__(self, encoder: RedisFieldEncoder) -> None:
        self._encoder = encoder

    def build_query(self, search_params: VDBKNNSearchParams) -> RedisQuery:
        vector_field_param_name = f"{search_params.vector_field.name}_param"
        query_string = self._create_query_string(search_params, vector_field_param_name)
        query = self._init_query(query_string, search_params.limit, search_params.fields_to_return)
        query_vector = self._encoder.encode_field(search_params.vector_field)
        query_params = {vector_field_param_name: query_vector}
        return RedisQuery(query, query_params)

    def _compile_filters_to_redis_filters(self, filters: Sequence[ComparisonOperation[Field]]) -> Sequence[RedisFilter]:
        return [self._compile_filter(filter_) for filter_ in filters]

    def _compile_filter(self, filter_: ComparisonOperation[Field]) -> RedisFilter:
        other = (
            self._get_other_as_sequence(filter_._other) if filter_._op in LIST_TYPE_COMPATIBLE_TYPES else filter_._other
        )
        field_value = (
            self._encode_iterable_field(filter_._operand, other)
            if filter_._op in ITERABLE_COMPARISON_OPERATION_TYPES
            else self._encode_field(filter_._operand, other)
        )
        return RedisFilter(cast(Field, filter_._operand), field_value, filter_._op)

    def _encode_iterable_field(self, operand: ComparisonOperand, other: Any) -> list[RedisEncodedTypes]:
        return [self._encode_field(operand, item) for item in other]

    def _get_other_as_sequence(self, other: Any) -> Sequence[Any]:
        if TypeValidator.is_sequence_safe(other):
            return cast(Sequence, other)
        return [other]

    def _encode_field(self, operand: ComparisonOperand, other: object) -> RedisEncodedTypes:
        return self._encoder.encode_field(FieldData.from_field(cast(Field, operand), other))

    def _create_query_string(
        self,
        search_params: VDBKNNSearchParams,
        vector_field_param_name: str,
    ) -> str:
        pre_filter_str = self.calculate_pre_filters_str(search_params, vector_field_param_name)
        return (
            f"{pre_filter_str}=>[KNN {search_params.limit} "
            + f"@{search_params.vector_field.name} ${vector_field_param_name} AS {VECTOR_DISTANCE_ALIAS}]"
        )

    def calculate_pre_filters_str(
        self,
        search_params: VDBKNNSearchParams,
        vector_field_param_name: str,
    ) -> str:
        grouped_filters = ComparisonOperation._group_filters_by_group_key(search_params.filters or [])
        prefixes_by_group: dict[int | None, list[str]] = {
            group_key: [redis_filter.get_prefix() for redis_filter in self._compile_filters_to_redis_filters(filters)]
            for group_key, filters in grouped_filters.items()
        }
        if search_params.radius is not None:
            if None not in prefixes_by_group:
                prefixes_by_group[None] = []
            radius_filter_str = self._create_radius_filter_str(
                search_params.vector_field,
                search_params.radius,
                vector_field_param_name,
            )
            prefixes_by_group[None].append(radius_filter_str)
        grouped_prefixes = [
            f"({(' ' if group_key is None else '|').join(prefixes)})"
            for group_key, prefixes in prefixes_by_group.items()
        ]
        if not grouped_prefixes:
            return "*"
        if len(grouped_prefixes) == 1:
            return grouped_prefixes[0]
        return f"({' '.join(grouped_prefixes)})"

    def _init_query(self, query_string: str, limit: int, fields_to_return: Sequence[Field]) -> Query:
        return (
            Query(query_string)
            .sort_by(VECTOR_DISTANCE_ALIAS, asc=True)
            .paging(0, limit)
            .return_fields(
                *(
                    [VECTOR_DISTANCE_ALIAS, RANGE_DISTANCE_PARAM_NAME]
                    + [returned_field.name for returned_field in fields_to_return]
                )
            )
            .dialect(2)
        )

    def _create_radius_filter_str(
        self,
        vector_field: VectorFieldData,
        radius: float,
        vector_field_param_name: str,
    ) -> str:
        # Radius won't work perfectly on indices with IP distance metric!
        return (
            f"@{vector_field.name}:[VECTOR_RANGE {radius} ${vector_field_param_name}]"
            + f"=>{{$yield_distance_as: {RANGE_DISTANCE_PARAM_NAME}}}"
        )
