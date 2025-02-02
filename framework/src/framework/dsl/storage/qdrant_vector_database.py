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
from qyver.framework.storage.common.vdb_settings import VDBSettings
from qyver.framework.storage.qdrant.qdrant_connection_params import (
    QdrantConnectionParams,
)
from qyver.framework.storage.qdrant.qdrant_vdb_connector import QdrantVDBConnector


class QdrantVectorDatabase(VectorDatabase[QdrantVDBConnector]):
    """
    Qdrant implementation of the VectorDatabase.

    This class provides a Qdrant-based vector database connector.
    """

    def __init__(self, url: str, api_key: str, default_query_limit: int = 10, **extra_params: Any) -> None:
        """
        Initialize the QdrantVectorDatabase.

        Args:
            url (str): The url of the Qdrant server.
            api_key (str): The api key of the Qdrant cluster.
            default_query_limit (int): Default vector search limit, set to Qdrant's default of 10.
            **extra_params (Any): Additional parameters for the Qdrant connection.
        """
        super().__init__()
        self._connection_params = QdrantConnectionParams(url, api_key, **extra_params)
        self._settings = VDBSettings(default_query_limit)

    @property
    def _vdb_connector(self) -> QdrantVDBConnector:
        """
        Get the Qdrant vector database connector.

        Returns:
            QdrantVDBConnector: The Qdrant vector database connector instance.
        """
        return QdrantVDBConnector(self._connection_params, self._settings)
