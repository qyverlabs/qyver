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


import json

import structlog
from beartype.typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import override

from qyver.framework.common.util.singleton_decorator import singleton

logger = structlog.getLogger()


@singleton
class Settings(BaseSettings):
    APP_ID: str = "default"
    ONLINE_PUT_CHUNK_SIZE: int = 10000
    MODEL_CACHE_DIR: str | None = None
    SENTENCE_TRANSFORMERS_MODEL_LOCK_MAX_RETRIES: int = 10
    SENTENCE_TRANSFORMERS_MODEL_LOCK_RETRY_DELAY: int = 1
    GPU_EMBEDDING_THRESHOLD: int = 0
    DISABLE_RICH_TRACEBACK: bool = False
    qyver_LOG_LEVEL: int | str | None = None
    qyver_LOG_AS_JSON: bool = False
    qyver_LOG_FILE_PATH: str | None = None
    qyver_EXPOSE_PII: bool = False
    # QUEUE specific params
    QUEUE_MODULE_PATH: str | None = None
    QUEUE_CLASS_NAME: str | None = None
    QUEUE_CLASS_ARGS_STR: str | None = None
    QUEUE_CLASS_ARGS: dict[str, Any] | None = None
    INGESTION_TOPIC_NAME: str | None = None
    QUEUE_MESSAGE_VERSION: int = 1
    REQUEST_TIMEOUT: int = 600  # 10min
    # STORAGE specific params
    BLOB_HANDLER_MODULE_PATH: str | None = None
    BLOB_HANDLER_CLASS_NAME: str | None = None
    BLOB_HANDLER_CLASS_ARGS_STR: str | None = None
    BLOB_HANDLER_CLASS_ARGS: dict[str, Any] | None = None
    INIT_SEARCH_INDICES: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @override
    def model_post_init(self, __context: Any) -> None:
        self.QUEUE_CLASS_ARGS = self.__parse_class_args(self.QUEUE_CLASS_ARGS_STR)  # pylint: disable=invalid-name
        self.__warn_for_incomplete_queue_params()

        self.BLOB_HANDLER_CLASS_ARGS = self.__parse_class_args(  # pylint: disable=invalid-name
            self.BLOB_HANDLER_CLASS_ARGS_STR
        )
        self.__warn_for_incomplete_blob_params()

    def __parse_class_args(self, string_args: str | None) -> dict | None:
        if string_args:
            try:
                return json.loads(string_args)
            except json.JSONDecodeError as e:
                logger.warning(e)
        return None

    def __warn_for_incomplete_queue_params(self) -> None:
        queue_params = {
            "QUEUE_MODULE_PATH": self.QUEUE_MODULE_PATH,
            "QUEUE_CLASS_NAME": self.QUEUE_CLASS_NAME,
            "QUEUE_CLASS_ARGS": self.QUEUE_CLASS_ARGS,
            "INGESTION_TOPIC_NAME": self.INGESTION_TOPIC_NAME,
        }
        if any(value is not None for value in queue_params.values()) and not all(
            value is not None for value in queue_params.values()
        ):
            logger.warning(
                "Queue configuration warning: Incomplete queue parameters detected. "
                "Ensure all parameters are set for proper queue functionality.",
                params=queue_params,
            )

    def __warn_for_incomplete_blob_params(self) -> None:
        blob_params = {
            "BLOB_HANDLER_MODULE_PATH": self.BLOB_HANDLER_MODULE_PATH,
            "BLOB_HANDLER_CLASS_NAME": self.BLOB_HANDLER_CLASS_NAME,
            "BLOB_HANDLER_CLASS_ARGS": self.BLOB_HANDLER_CLASS_ARGS,
        }
        if any(value is not None for value in blob_params.values()) and not all(
            value is not None for value in blob_params.values()
        ):
            logger.warning(
                "Blob handler configuration warning: Incomplete blob handler parameters detected. "
                "Ensure all parameters are set for proper blob handler functionality.",
                params=blob_params,
            )
