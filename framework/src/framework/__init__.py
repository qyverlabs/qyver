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


try:
    # altair dependency is optional
    from qyver.evaluation.charts.recency_plotter import RecencyPlotter
except ImportError:
    pass

try:
    # pymongo dependency is optional
    from qyver.framework.dsl.storage.mongo_db_vector_database import (
        MongoDBVectorDatabase,
    )
except ImportError:
    pass

try:
    # qdrant dependency is optional
    from qyver.framework.dsl.storage.qdrant_vector_database import (
        QdrantVectorDatabase,
    )
except ImportError:
    pass

try:
    # redis dependency is optional
    from qyver.framework.dsl.storage.redis_vector_database import (
        RedisVectorDatabase,
    )
except ImportError:
    pass
from qyver.evaluation.pandas_converter import PandasConverter
from qyver.evaluation.vector_sampler import VectorSampler
from qyver.framework.blob.blob_handler_factory import BlobHandlerConfig
from qyver.framework.common.dag.context import CONTEXT_COMMON, CONTEXT_COMMON_NOW
from qyver.framework.common.dag.period_time import PeriodTime
from qyver.framework.common.nlq.open_ai import OpenAIClientConfig
from qyver.framework.common.parser.dataframe_parser import DataFrameParser
from qyver.framework.common.parser.json_parser import JsonParser
from qyver.framework.common.schema.event_schema import EventSchema, event_schema
from qyver.framework.common.schema.event_schema_object import (
    CreatedAtField,
    SchemaReference,
)
from qyver.framework.common.schema.id_schema_object import IdField
from qyver.framework.common.schema.schema import Schema, schema
from qyver.framework.common.schema.schema_object import (
    Blob,
    Float,
    FloatList,
    Integer,
    String,
    StringList,
    Timestamp,
)
from qyver.framework.common.space.config.embedding.image_embedding_config import (
    ModelHandler,
)
from qyver.framework.common.space.config.embedding.number_embedding_config import (
    LinearScale,
    LogarithmicScale,
    Mode,
)
from qyver.framework.common.util.interactive_util import get_altair_renderer
from qyver.framework.dsl.app.interactive.interactive_app import InteractiveApp
from qyver.framework.dsl.executor.in_memory.in_memory_executor import (
    InMemoryApp,
    InMemoryExecutor,
)
from qyver.framework.dsl.executor.interactive.interactive_executor import (
    InteractiveExecutor,
)
from qyver.framework.dsl.executor.rest.rest_configuration import RestQuery
from qyver.framework.dsl.executor.rest.rest_descriptor import RestDescriptor
from qyver.framework.dsl.executor.rest.rest_executor import RestExecutor
from qyver.framework.dsl.index.effect import Effect
from qyver.framework.dsl.index.index import Index
from qyver.framework.dsl.query.param import Param
from qyver.framework.dsl.query.query import Query
from qyver.framework.dsl.query.result import QueryResult
from qyver.framework.dsl.registry.qyver_registry import qyverRegistry
from qyver.framework.dsl.source.data_loader_source import (
    DataFormat,
    DataLoaderConfig,
    DataLoaderSource,
)
from qyver.framework.dsl.source.in_memory_source import InMemorySource
from qyver.framework.dsl.source.interactive_source import InteractiveSource
from qyver.framework.dsl.source.rest_source import RestSource
from qyver.framework.dsl.space.categorical_similarity_space import (
    CategoricalSimilaritySpace,
)
from qyver.framework.dsl.space.custom_space import CustomSpace
from qyver.framework.dsl.space.image_space import ImageSpace
from qyver.framework.dsl.space.number_space import NumberSpace
from qyver.framework.dsl.space.recency_space import RecencySpace
from qyver.framework.dsl.space.text_similarity_space import (
    TextSimilaritySpace,
    chunk,
)
from qyver.framework.dsl.storage.in_memory_vector_database import (
    InMemoryVectorDatabase,
)

__all__ = [
    # Evaluation
    "PandasConverter",
    "RecencyPlotter",
    "VectorSampler",
    # Framework Common recency
    "CONTEXT_COMMON",
    "CONTEXT_COMMON_NOW",
    "PeriodTime",
    # Framework Common nlq
    "OpenAIClientConfig",
    # Framework Common util
    "get_altair_renderer",
    # Framework Common parsers
    "DataFrameParser",
    "JsonParser",
    # Framework Common schema parents
    "EventSchema",
    "Schema",
    # Framework Common schema decorators
    "event_schema",
    "schema",
    # Framework Common Fields
    "Blob",
    "CreatedAtField",
    "Float",
    "FloatList",
    "IdField",
    "Integer",
    "SchemaReference",
    "String",
    "StringList",
    "Timestamp",
    # Number Space Config
    "Mode",
    # DB
    "InMemoryVectorDatabase",
    "MongoDBVectorDatabase",
    "QdrantVectorDatabase",
    "RedisVectorDatabase",
    # Data loader
    "DataFormat",
    "DataLoaderConfig",
    "DataLoaderSource",
    # DSL App
    "InteractiveApp",
    "InMemoryApp",
    # DSL Executor
    "InMemoryExecutor",
    "InteractiveExecutor",
    "RestExecutor",
    # DSL Source
    "InteractiveSource",
    "InMemorySource",
    "RestSource",
    # DSL Index
    "Effect",
    "Index",
    # DSL Query
    "Param",
    "Query",
    "RestQuery",
    "QueryResult",
    # DSL Space
    "CategoricalSimilaritySpace",
    "CustomSpace",
    "ImageSpace",
    "NumberSpace",
    "RecencySpace",
    "TextSimilaritySpace",
    # DSL Executor util
    "RestDescriptor",
    # DSL ImageSpace util
    "ModelHandler",
    # DSL TextSimilaritySpace util
    "chunk",
    # DSL NumberSpace util
    "LinearScale",
    "LogarithmicScale",
    # misc
    "qyverRegistry",
    "BlobHandlerConfig",
]

from qyver.framework.common.qyver_logging import (
    qyverLoggerConfigurator,
)

qyverLoggerConfigurator.configure_default_logger()
