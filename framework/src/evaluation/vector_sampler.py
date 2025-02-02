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

import numpy as np
from beartype.typing import Any, Sequence, cast
from scipy import linalg

from qyver.framework.common.data_types import NPArray, Vector
from qyver.framework.common.interface.has_length import HasLength
from qyver.framework.common.schema.id_schema_object import IdSchemaObject
from qyver.framework.common.schema.schema_object import SchemaObject
from qyver.framework.common.storage_manager.header import Header
from qyver.framework.dsl.executor.in_memory.in_memory_executor import InMemoryApp
from qyver.framework.dsl.index.index import Index
from qyver.framework.dsl.space.space import Space
from qyver.framework.storage.in_memory.in_memory_vdb import InMemoryVDB


class VectorNotFoundError(Exception):
    pass


class VectorCollection:
    """
    Dataclass containing ids in a list, and vectors in a np.array. It is always true that `self.id_list[i]` is the id of
    the object of which `self.vectors[i]` is the embedded vector.

    Attributes:
        id_list (list[str]): List of object ids.
        vectors (np.ndarray[Any, np.dtype[np.float32]]): Numpy array of floats.
    """

    def __init__(self, id_list: Sequence[str], vectors: NPArray) -> None:
        if (len(id_list) > 1) & (len(id_list) != vectors.shape[0]):
            raise ValueError(
                f"id_list length and vectors parameter shape's first dimension should match. "
                f"Got {id_list=} and {vectors.shape[0]=}"
            )
        self.id_list: Sequence[str] = id_list
        self.vectors: NPArray = vectors

    def __len__(self) -> int:
        return len(self.id_list)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, VectorCollection):
            return (self.id_list == other.id_list) & np.allclose(self.vectors, other.vectors)
        return False

    def __str__(self) -> str:
        num_vectors: int = len(self.id_list)
        return f"VectorCollection of {num_vectors} vector{'s.' if num_vectors > 1 else '.'}"

    def __repr__(self) -> str:
        return self.__str__()


class VectorSampler:
    """
    VectorSampler is a class that provides methods to retrieve vectors from an App instance.
    It's important to note that this is intended for use exclusively with InMemoryStorage.

    Attributes:
        __app: An instance of InMemoryApp.

    Methods:
        __init__(self, app: InMemoryApp): Initializes a new instance of the VectorSampler class.

        get_vectors_by_ids(self, id_: str, index: Index, schema: IdSchemaObject) -> VectorCollection:
            Retrieves the vector of an entity by its id, schema, and the index it's stored in.
            If no entity is found, a VectorNotFoundError is raised.

        get_all_vectors(self, index: Index, schema: IdSchemaObject) -> ndarray:
            Retrieves all vectors for each entity in a given schema and the index it's stored in.
            If no entities are found, a VectorNotFoundError is raised.
    """

    def __init__(self, app: InMemoryApp) -> None:
        """
        Initializes a new instance of the VectorSampler class.

        Args:
            app (InMemoryApp): An instance of InMemoryApp.
        """
        self.__app = app

    @staticmethod
    def apply_weights_on_vectors(
        vector: Vector,
        schema: SchemaObject,
        spaces: Sequence[Space],
        weight_dict: dict[Space, float],
    ) -> Vector:
        if isinstance(spaces, Space):
            spaces = [spaces]

        vector_value: np.ndarray = vector.replace_negative_filters(0).value
        if linalg.norm(vector_value) == 0:
            return vector

        lengths = np.array(
            [
                node.length
                for node in [space._get_embedding_node(schema) for space in spaces]
                if isinstance(node, HasLength)
            ]
        )
        weights = [weight_dict.get(space, 1) for space in spaces]
        vector_slices = np.split(vector_value, list(lengths.cumsum()))
        weighted_vector_values = np.concatenate(
            [vector_slice * weight for vector_slice, weight in zip(vector_slices, weights)]
        )
        normalized_vector_values = weighted_vector_values / linalg.norm(weighted_vector_values)
        vector.value[vector.non_negative_filter_mask] = normalized_vector_values[vector.non_negative_filter_mask]

        return vector

    def get_vectors_by_ids(
        self,
        id_: str | list[str],
        index: Index,
        schema: IdSchemaObject,
        weight_dict: dict[Space, float] | None = None,
        readable_id_: str | list[str] | None = None,
    ) -> VectorCollection:
        """
        Retrieves an entity's vector by its id, schema, and the index it's stored in.

        Args:
            id_ (str) | list(str): The id(s) of the entity(ies).
            index (Index): The index in which the entity is stored.
            schema (IdSchemaObject): The schema of the entity.
            weight_dict (dict[Space, float]): Dictionary containing weights per spaces.
                Defaults to uniform unit weights.
            readable_id_ (str) | list(str): The readable id of the entity(ies). For chunks, it is constructed from the
                origin_id (entity from which it originates from) and the chunk id. Defaults to using the ids.

        Returns:
            VectorCollection: The vectors corresponding to the given id(s), index, and schema.

        Raises:
            VectorNotFoundError: If no entity is found.
        """
        ids = [id_] if isinstance(id_, str) else id_
        if readable_id_ is None:
            readable_ids = ids
        else:
            readable_ids = [readable_id_] if isinstance(readable_id_, str) else readable_id_
        if len(ids) != len(readable_ids):
            raise ValueError(
                f"id_ and readable_id_ should have the same length. " f"Got {len(ids)} and {len(readable_ids)}"
            )

        entity_vectors: list[NPArray] = []
        entity_ids: list[str] = []
        for identification, readable_id in zip(ids, readable_ids):
            vector: Vector | None = self.__app.storage_manager.read_node_result(
                schema, identification, index._node.node_id, index._node.node_data_type
            )
            if vector is None:
                raise VectorNotFoundError(
                    f"No vector found for {schema._schema_name} with id {identification} in the given index."
                )

            weighted_vector = (
                self.apply_weights_on_vectors(
                    vector,
                    schema,
                    index._spaces,
                    weight_dict,
                )
                if weight_dict
                else vector
            )
            entity_vectors.append(np.array(weighted_vector.value))
            entity_ids.append(readable_id)

        return VectorCollection(entity_ids, np.array(entity_vectors))

    def get_all_vectors(
        self,
        index: Index,
        schema: IdSchemaObject,
        weight_dict: dict[Space, float] | None = None,
        include_chunks: bool = False,
    ) -> VectorCollection:
        """
        Retrieves all entities and their vectors for a given schema and the index they're stored in.

        Args:
            index (Index): The index in which the entities are stored.
            schema (IdSchemaObject): The schema of the entities.
            weight_dict (dict[Space, float]): Dictionary containing weights per spaces.
                Defaults to uniform unit weights for each space.
            include_chunks (bool): Whether to include vectors of chunks present in the index. Chunks are created if
                the index contains a TextSimilaritySpace that is chunked.

        Returns:
            VectorCollection: All vectors for each corresponding entity to the given index and schema and a list of
                ids. Position `i` in the id list correspond to row `i` in the vector array.

        Raises:
            VectorNotFoundError: If no vector is found for any entities.
        """
        headers = self._read_node_results(schema, index._node.node_id, index._node.node_data_type)
        if include_chunks:
            entity_ids: list[str] = [header.object_id for header in headers]
            readable_ids: list[str] = [self.human_readable_id_for_chunks(header) for header in headers]
            return self.get_vectors_by_ids(entity_ids, index, schema, weight_dict, readable_ids)

        entity_ids = list({self.__get_id_for_standalone_entity_origin_id_for_chunk(header) for header in headers})
        return self.get_vectors_by_ids(entity_ids, index, schema)

    def _read_node_results(self, schema: SchemaObject, node_id: str, result_type: type) -> Sequence[Header]:
        entity_builder = self.__app.storage_manager._entity_builder
        in_memory_vdb = cast(InMemoryVDB, self.__app.storage_manager._vdb_connector)

        schema_filter = entity_builder._admin_fields.schema_id.field == schema._schema_name
        result_field = entity_builder.compose_field(node_id, result_type)
        fields_to_return = entity_builder._admin_fields.header_fields
        entity_data = in_memory_vdb.read_entities_matching_filters([schema_filter], [result_field], fields_to_return)
        return [entity_builder._admin_fields.extract_header(ed.field_data) for ed in entity_data]

    @staticmethod
    def __get_id_for_standalone_entity_origin_id_for_chunk(
        header: Header,
    ) -> str:
        if header.origin_id is not None:
            return header.origin_id
        return header.object_id

    @staticmethod
    def human_readable_id_for_chunks(header: Header) -> str:
        if header.origin_id is not None:
            return f"{header.origin_id}-{header.object_id}"
        return header.object_id

    def __str__(self) -> str:
        return f"VectorSampler on app: {print(self.__app)}"

    def __repr__(self) -> str:
        return self.__str__()
