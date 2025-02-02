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
from enum import Enum, auto

from beartype.typing import Any, Generic, cast

from qyver.framework.common.parser.data_parser import DataParser
from qyver.framework.common.parser.dataframe_parser import DataFrameParser
from qyver.framework.common.schema.id_schema_object import IdSchemaObjectT
from qyver.framework.common.source.types import SourceTypeT
from qyver.framework.online.source.online_source import OnlineSource


class DataFormat(Enum):
    CSV = auto()
    FWF = auto()
    XML = auto()
    JSON = auto()
    PARQUET = auto()
    ORC = auto()


@dataclass
class DataLoaderConfig:
    path: str
    format: DataFormat
    name: str | None = None
    pandas_read_kwargs: dict[str, Any] | None = None


class DataLoaderSource(OnlineSource[IdSchemaObjectT, SourceTypeT], Generic[IdSchemaObjectT, SourceTypeT]):
    def __init__(
        self,
        schema: IdSchemaObjectT,
        data_loader_config: DataLoaderConfig,
        parser: DataParser[IdSchemaObjectT, SourceTypeT] | None = None,
    ):
        super().__init__(
            schema,
            cast(
                DataParser[IdSchemaObjectT, SourceTypeT],
                parser or DataFrameParser(schema),
            ),
        )
        self.__data_loader_config = data_loader_config

    @property
    def config(self) -> DataLoaderConfig:
        return self.__data_loader_config

    @property
    def name(self) -> str:
        return self.config.name or self._schema._schema_name
