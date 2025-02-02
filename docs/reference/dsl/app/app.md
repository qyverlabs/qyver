Module qyver.framework.dsl.app.app
========================================

Classes
-------

`App(sources: Sequence[~SourceT], indices: Sequence[qyver.framework.dsl.index.index.Index], vector_database: qyver.framework.dsl.storage.vector_database.VectorDatabase, context: qyver.framework.common.dag.context.ExecutionContext, init_search_indices: bool)`
:   Abstract base class for an App, a running executor that can, for example, do queries or ingest data.
    
    Initialize the App.
    Args:
        sources (list[SourceT]): The list of sources.
        indices (list[Index]): The list of indices.
        vector_database (VectorDatabase): The vector database which the executor will use.
        context (Mapping[str, Mapping[str, Any]]): The context mapping.

    ### Ancestors (in MRO)

    * abc.ABC
    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.app.online.online_app.OnlineApp

    ### Instance variables

    `storage_manager: qyver.framework.common.storage_manager.storage_manager.StorageManager`
    :   Get the storage manager.
        Returns:
            StorageManager: The storage manager instance.
