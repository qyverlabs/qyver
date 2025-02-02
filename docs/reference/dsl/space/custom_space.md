Module qyver.framework.dsl.space.custom_space
===================================================

Classes
-------

`CustomSpace(vector: qyver.framework.common.schema.schema_object.FloatList | None | collections.abc.Sequence[qyver.framework.common.schema.schema_object.FloatList | None], length: int, description: str | None = None)`
:   CustomSpace is the instrument of ingesting your own vectors into qyver.
    This way you can use your own vectors right away. What you need to know: (you can use numbering too)
    - vectors need to have the same length
    - vectors will be L2Norm normalized to ensure weighting makes sense
    - weighting can be performed (query-time)
    - you are going to need an FloatList typed SchemaField to supply your data
    - the FloatList field will be able to parse any Sequence[float | int]
    
    Initializes a CustomSpace for vector storage and manipulation within qyver.
    
    This constructor sets up a space designed for custom vector ingestion, allowing users to specify how these
    vectors are aggregated and normalized.
    
    Args:
        vector (FloatList | list[FloatList]): The input vector(s) to be stored in the space.
          This can be a single FloatList SchemaField or a list of those.
        length (int): The fixed length that all vectors in this space must have. This ensures uniformity and
          consistency in vector operations.

    ### Ancestors (in MRO)

    * qyver.framework.dsl.space.space.Space
    * qyver.framework.common.space.interface.has_transformation_config.HasTransformationConfig
    * qyver.framework.common.interface.has_length.HasLength
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * qyver.framework.dsl.space.has_space_field_set.HasSpaceFieldSet
    * abc.ABC

    ### Instance variables

    `space_field_set: qyver.framework.dsl.space.space_field_set.SpaceFieldSet`
    :

    `transformation_config: qyver.framework.common.space.config.transformation_config.TransformationConfig[qyver.framework.common.data_types.Vector, qyver.framework.common.data_types.Vector]`
    :
