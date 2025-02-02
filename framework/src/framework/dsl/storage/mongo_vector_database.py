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

from qyver.framework.dsl.storage.vector_database import VectorDatabase
from qyver.framework.storage.mongo.mongo_connection_params import (
    MongoConnectionParams,
)
from qyver.framework.storage.mongo.mongo_vdb_connector import MongoVDBConnector
from qyver.framework.storage.mongo.search_index.mongo_admin_params import (
    MongoAdminParams,
)


class MongoVectorDatabase(VectorDatabase[MongoVDBConnector]):
    """
    MongoDB implementation of the VectorDatabase.

    This class provides a MongoDB-based vector database connector.
    """

    def __init__(  # pylint: disable=R0913
        self,
        host: str,
        db_name: str,
        cluster_name: str,
        project_id: str,
        admin_api_user: str,
        admin_api_password: str,
        **extra_params: Any
    ) -> None:
        """
        Initialize the MongoVectorDatabase.

        Args:
            host (str): The hostname of the MongoDB server.
            db_name (str): The name of the database.
            cluster_name (str): The name of the MongoDB cluster.
            project_id (str): The project ID for MongoDB.
            admin_api_user (str): The admin API username.
            admin_api_password (str): The admin API password.
            **extra_params (Any): Additional parameters for the MongoDB connection.
        """
        super().__init__()
        self.__connection_params = MongoConnectionParams(
            host,
            db_name,
            MongoAdminParams(
                cluster_name, project_id, admin_api_user, admin_api_password
            ),
            **extra_params
        )
        self.__vdb_connector = MongoVDBConnector(self.__connection_params)

    @property
    def _vdb_connector(self) -> MongoVDBConnector:
        """
        Get the MongoDB vector database connector.

        Returns:
            MongoVDBConnector: The MongoDB vector database connector instance.
        """
        return self.__vdb_connector
