Module qyver.framework.dsl.space.space
============================================

Classes
-------

`Space(fields: Sequence[SchemaField], type_: type | TypeAlias)`
:   Abstract base class for a space.
    
    This class defines the interface for a space in the context of the application.

    ### Ancestors (in MRO)

    * qyver.framework.common.space.interface.has_transformation_config.HasTransformationConfig
    * qyver.framework.common.interface.has_length.HasLength
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * abc.ABC

    ### Descendants

    * qyver.framework.dsl.space.categorical_similarity_space.CategoricalSimilaritySpace
    * qyver.framework.dsl.space.custom_space.CustomSpace
    * qyver.framework.dsl.space.image_space.ImageSpace
    * qyver.framework.dsl.space.number_space.NumberSpace
    * qyver.framework.dsl.space.recency_space.RecencySpace
    * qyver.framework.dsl.space.text_similarity_space.TextSimilaritySpace

    ### Instance variables

    `allow_similar_clause: bool`
    :

    `annotation: str`
    :

    `length: int`
    :
