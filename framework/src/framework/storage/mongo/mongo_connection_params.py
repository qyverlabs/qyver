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

from beartype.typing import Any
from typing_extensions import override

from qyver.framework.storage.common.connection_params import ConnectionParams
from qyver.framework.storage.mongo.search_index.mongo_admin_params import (
    MongoAdminParams,
)

URL_PREFIX = "mongodb+srv://"


class MongoConnectionParams(ConnectionParams):
    def __init__(
        self,
        host: str,
        db_name: str,
        admin_params: MongoAdminParams,
        **extra_params: Any,
    ) -> None:
        super().__init__()
        user_pwd = self.__pop_user_pwd(extra_params)
        extra_params_str = self.get_uri_params_string(**extra_params)
        self._connection_string = f"{URL_PREFIX}{user_pwd}{host}{extra_params_str}"
        self.__db_name = db_name
        self.__admin_params = admin_params

    @override
    @property
    def connection_string(self) -> str:
        return self._connection_string

    @property
    def admin_params(self) -> MongoAdminParams:
        return self.__admin_params

    @property
    def db_name(self) -> str:
        return self.__db_name

    def __pop_user_pwd(self, extra_params: dict[str, Any]) -> str:
        user = extra_params.pop("username", "")
        pwd = extra_params.pop("password", "")
        return f"{user}:{pwd}@" if user and pwd else ""
