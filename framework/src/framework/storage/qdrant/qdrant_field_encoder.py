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
from beartype.typing import Any, Callable, Sequence, TypeVar

from qyver.framework.common.data_types import Vector
from qyver.framework.common.schema.blob_information import BlobInformation
from qyver.framework.common.storage.exception import EncoderException
from qyver.framework.common.storage.field.field import Field
from qyver.framework.common.storage.field.field_data import FieldData
from qyver.framework.common.storage.field.field_data_type import FieldDataType

QdrantEncodedTypes = str | float | int | Sequence[float] | dict[str, Any] | Sequence[str]
QdrantEncodedT = TypeVar("QdrantEncodedT", bound=QdrantEncodedTypes)


class QdrantFieldEncoder:
    def __init__(self) -> None:
        # TODO FAI-1909
        self._encode_map: dict[FieldDataType, Callable[..., Any]] = {
            FieldDataType.BLOB: self._encode_blob,
            FieldDataType.DOUBLE: self._encode_base_type,
            FieldDataType.FLOAT_LIST: self._encode_base_type,
            FieldDataType.INT: self._encode_base_type,
            FieldDataType.JSON: self._encode_base_type,
            FieldDataType.STRING: self._encode_base_type,
            FieldDataType.STRING_LIST: self._encode_base_type,
            FieldDataType.VECTOR: self._encode_vector,
        }
        self._decode_map: dict[FieldDataType, Callable[..., Any]] = {
            FieldDataType.BLOB: self._decode_blob,
            FieldDataType.DOUBLE: self._decode_base_type,
            FieldDataType.FLOAT_LIST: self._decode_base_type,
            FieldDataType.INT: self._decode_base_type,
            FieldDataType.JSON: self._decode_base_type,
            FieldDataType.STRING: self._decode_base_type,
            FieldDataType.STRING_LIST: self._decode_base_type,
            FieldDataType.VECTOR: self._decode_vector,
        }

    def _encode_base_type(self, base_type: QdrantEncodedT) -> QdrantEncodedT:
        return base_type

    def _decode_base_type(self, base_type: QdrantEncodedT) -> QdrantEncodedT:
        return base_type

    def _encode_blob(self, blob: BlobInformation) -> str | None:
        return blob.path

    def _decode_blob(self, blob: str) -> BlobInformation:
        return BlobInformation(path=blob)

    def _encode_vector(self, vector: Vector) -> list[float]:
        np_vector: np.ndarray
        if isinstance(vector.value, np.ndarray):
            np_vector = vector.value.astype(np.float32)
        else:
            np_vector = np.array(vector.value, dtype=np.float32)
        return np_vector.tolist()

    def _decode_vector(self, vector: list[float]) -> Vector:
        return Vector(vector)

    def encode_field(self, field: FieldData) -> QdrantEncodedTypes:
        if encoder := self._encode_map.get(field.data_type):
            return encoder(field.value)
        raise EncoderException(f"Unknown field type: {field.data_type}, cannot encode field.")

    def decode_field(self, field: Field, value: Any) -> FieldData:
        if decoder := self._decode_map.get(field.data_type):
            return FieldData.from_field(field, decoder(value))
        raise EncoderException(f"Unknown field type: {field.data_type}, cannot decode field.")
