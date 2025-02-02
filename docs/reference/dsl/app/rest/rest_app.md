Module qyver.framework.dsl.app.rest.rest_app
==================================================

Classes
-------

`RestApp(sources: Sequence[qyver.framework.dsl.source.rest_source.RestSource | qyver.framework.dsl.source.data_loader_source.DataLoaderSource], indices: Sequence[qyver.framework.dsl.index.index.Index], queries: Sequence[qyver.framework.dsl.executor.rest.rest_configuration.RestQuery], vector_database: qyver.framework.dsl.storage.vector_database.VectorDatabase, context: qyver.framework.common.dag.context.ExecutionContext, endpoint_configuration: qyver.framework.dsl.executor.rest.rest_configuration.RestEndpointConfiguration, queue: qyver.framework.queue.interface.queue.Queue[qyver.framework.queue.interface.queue_message.MessageBody[dict]] | None = None, blob_handler: qyver.framework.blob.blob_handler.BlobHandler | None = None)`
:   Rest implementation of the App class.
    
    Initialize the RestApp from a RestExecutor.
    
    Args:
        sources (Sequence[RestSource | DataLoaderSource]): The list of sources, which can be either
            RestSource or DataLoaderSource.
        indices (Sequence[Index]): The list of indices to be used by the RestApp.
        queries (Sequence[RestQuery]): The list of queries to be executed by the RestApp.
        vector_database (VectorDatabase): The vector database instance to be used by the RestApp.
        context (ExecutionContext): The execution context for the RestApp.
        endpoint_configuration (RestEndpointConfiguration): The configuration for the REST endpoints.
        queue (Queue[dict] | None): a messaging queue persisting the ingested data; defaults to None.

    ### Ancestors (in MRO)

    * qyver.framework.dsl.app.online.online_app.OnlineApp
    * qyver.framework.dsl.app.app.App
    * abc.ABC
    * typing.Generic
    * qyver.framework.dsl.query.query_mixin.QueryMixin

    ### Instance variables

    `data_loader_sources: Sequence[qyver.framework.dsl.source.data_loader_source.DataLoaderSource]`
    :   Property that returns the list of DataLoaderSource instances associated with the RestApp.
        
        Returns:
            Sequence[DataLoaderSource]: A sequence of DataLoaderSource instances.

    `handler: qyver.framework.dsl.executor.rest.rest_handler.RestHandler`
    :   Property that returns the RestHandler instance associated with the RestApp.
        
        Returns:
            RestHandler: An instance of RestHandler.
