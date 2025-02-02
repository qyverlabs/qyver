Module qyver.framework.dsl.space.image_space
==================================================

Classes
-------

`ImageSpace(image: qyver.framework.common.schema.schema_object.Blob | qyver.framework.common.schema.schema_object.DescribedBlob | None | collections.abc.Sequence[qyver.framework.common.schema.schema_object.Blob | qyver.framework.common.schema.schema_object.DescribedBlob | None], model: str = 'clip-ViT-B-32', model_handler: qyver.framework.common.space.config.embedding.image_embedding_config.ModelHandler = ModelHandler.SENTENCE_TRANSFORMERS, model_cache_dir: pathlib.Path | None = None)`
:   Initialize the ImageSpace instance for generating vector representations
    from images, supporting models from the OpenCLIP project.
    
    Args:
        image (Blob | DescribedBlob | Sequence[Blob | DescribedBlob]):
            The image content as a Blob or DescribedBlob (write image+description), or a sequence of them.
        model (str, optional): The model identifier for generating image embeddings.
            Defaults to "clip-ViT-B-32".
        model_handler (ModelHandler, optional): The handler for the model,
            defaults to ModelHandler.SENTENCE_TRANSFORMERS.
    
    Raises:
        InvalidSpaceParamException: If the image and description fields are not
            from the same schema.
    
    Initialize the ImageSpace instance for generating vector representations
    from images, supporting models from the OpenCLIP project.
    
    Args:
        image (Blob | DescribedBlob | Sequence[Blob | DescribedBlob]):
            The image content as a Blob or DescribedBlob (write image+description), or a sequence of them.
        model (str, optional): The model identifier for generating image embeddings.
            Defaults to "clip-ViT-B-32".
        model_handler (ModelHandler, optional): The handler for the model,
            defaults to ModelHandler.SENTENCE_TRANSFORMERS.
        model_cache_dir (Path | None, optional): Directory to cache downloaded models.
            If None, uses the default cache directory. Defaults to None.
    
    Raises:
        InvalidSpaceParamException: If the image and description fields are not
            from the same schema.

    ### Ancestors (in MRO)

    * qyver.framework.dsl.space.space.Space
    * qyver.framework.common.space.interface.has_transformation_config.HasTransformationConfig
    * qyver.framework.common.interface.has_length.HasLength
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * abc.ABC

    ### Instance variables

    `transformation_config: qyver.framework.common.space.config.transformation_config.TransformationConfig[qyver.framework.common.data_types.Vector, qyver.framework.common.schema.image_data.ImageData]`
    :
