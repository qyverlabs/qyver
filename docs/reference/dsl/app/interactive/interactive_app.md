Module qyver.framework.dsl.app.interactive.interactive_app
================================================================

Classes
-------

`InteractiveApp(sources: Sequence[qyver.framework.dsl.source.interactive_source.InteractiveSource], indices: Sequence[qyver.framework.dsl.index.index.Index], vector_database: qyver.framework.dsl.storage.vector_database.VectorDatabase, context: qyver.framework.common.dag.context.ExecutionContext, init_search_indices: bool = True)`
:   Interactive implementation of the App class.
    
    Initialize the InteractiveApp from an InteractiveExecutor.
    Args:
        sources (list[InteractiveSource]): List of interactive sources.
        indices (list[Index]): List of indices.
        vector_database (VectorDatabase | None): Vector database instance. Defaults to InMemory.
        context (Mapping[str, Mapping[str, Any]]): Context mapping.
        init_search_indices (bool): Decides if the search indices need to be created. Defaults to True.

    ### Ancestors (in MRO)

    * qyver.framework.dsl.app.online.online_app.OnlineApp
    * qyver.framework.dsl.app.app.App
    * abc.ABC
    * typing.Generic
    * qyver.framework.dsl.query.query_mixin.QueryMixin

    ### Descendants

    * qyver.framework.dsl.app.in_memory.in_memory_app.InMemoryApp
