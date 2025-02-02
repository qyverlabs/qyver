Module qyver.framework.dsl.source.interactive_source
==========================================================

Classes
-------

`InteractiveSource(schema: ~IdSchemaObjectT, parser: qyver.framework.common.parser.data_parser.DataParser[~IdSchemaObjectT, ~SourceTypeT] | None = None)`
:   InteractiveSource represents a source of data, where you can put your data. This will supply
    the index with the data it needs to index and search in.
    
    Initialize the InteractiveSource.
    
    Args:
        schema (IdSchemaObject): The schema object.
        parser (DataParser | None, optional): The data parser. Defaults to JsonParser if None is supplied.
    
    Raises:
        InitializationException: If the schema is not an instance of SchemaObject.

    ### Ancestors (in MRO)

    * qyver.framework.online.source.online_source.OnlineSource
    * qyver.framework.common.observable.TransformerPublisher
    * qyver.framework.common.source.source.Source
    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.source.in_memory_source.InMemorySource

    ### Methods

    `allow_data_ingestion(self) ‑> None`
    :

    `put(self, data: SourceTypeT | Sequence[SourceTypeT]) ‑> None`
    :   Put data into the InteractiveSource. This operation can take time as the vectorization
        of your data happens here.
        
        Args:
            data (SourceTypeT | list[SourceTypeT]): The data to put.
