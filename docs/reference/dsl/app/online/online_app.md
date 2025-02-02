Module qyver.framework.dsl.app.online.online_app
======================================================

Classes
-------

`OnlineApp(sources: Sequence[~OnlineSourceT], indices: Sequence[qyver.framework.dsl.index.index.Index], vector_database: qyver.framework.dsl.storage.vector_database.VectorDatabase, context: qyver.framework.common.dag.context.ExecutionContext, init_search_indices: bool, queue: qyver.framework.queue.interface.queue.Queue | None = None, blob_handler: qyver.framework.blob.blob_handler.BlobHandler | None = None, query_result_converter: qyver.framework.dsl.query.query_result_converter.query_result_converter.QueryResultConverter | None = None)`
:   Manages the execution environment for online sources and indices.
    
    This class extends the base App class and incorporates the QueryMixin to handle
    query execution. It is designed to work with online sources and indices, providing
    the necessary setup and management for efficient data processing and querying.
    
    Initialize the OnlineApp with the given sources, indices, vector database, and execution context.
    
    Args:
        sources (Sequence[OnlineSourceT]): A sequence of data sources to be used by the application.
        indices (Sequence[Index]): A sequence of indices for data retrieval and storage.
        vector_database (VectorDatabase): The vector database instance for managing vector data.
        context (ExecutionContext): The execution context providing necessary runtime information.
        source_to_queue_map (dict[OnlineSourceT, Queue] | None): a mapping from sources
            to messaging queues persisting the ingested data on the given source; defaults to None.

    ### Ancestors (in MRO)

    * qyver.framework.dsl.app.app.App
    * abc.ABC
    * typing.Generic
    * qyver.framework.dsl.query.query_mixin.QueryMixin

    ### Descendants

    * qyver.framework.dsl.app.interactive.interactive_app.InteractiveApp
    * qyver.framework.dsl.app.rest.rest_app.RestApp

    ### Class variables

    `INGEST_MESSAGE_TYPE`
    :
