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

import logging

from qyver.framework.common.logging import PACKAGE_NAME, LoggerConfigurator
from qyver.framework.common.settings import Settings


class qyverLoggerConfigurator:
    @staticmethod
    def configure_default_logger() -> None:
        settings = Settings()
        if settings.qyver_LOG_LEVEL:
            logging.getLogger(PACKAGE_NAME).setLevel(settings.qyver_LOG_LEVEL)
        LoggerConfigurator.configure_default_logger(
            LoggerConfigurator._get_common_processors(settings.qyver_EXPOSE_PII)
        )

    @staticmethod
    def configure_structlog_logger() -> None:
        settings = Settings()
        if settings.qyver_LOG_LEVEL:
            logging.getLogger(PACKAGE_NAME).setLevel(settings.qyver_LOG_LEVEL)
        LoggerConfigurator.configure_structlog_logger(
            settings.qyver_LOG_FILE_PATH,
            expose_pii=settings.qyver_EXPOSE_PII,
            log_as_json=settings.qyver_LOG_AS_JSON,
        )
