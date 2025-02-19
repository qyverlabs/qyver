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

from pydantic_settings import BaseSettings, SettingsConfigDict

from qyver.framework.common.util.singleton_decorator import singleton


@singleton
class GCPSettings(BaseSettings):
    GCP_PROJECT_ID: str | None = None
    PUB_SUB_TIMEOUT: int | None = None

    model_config = SettingsConfigDict(env_file=".env-gcp")
