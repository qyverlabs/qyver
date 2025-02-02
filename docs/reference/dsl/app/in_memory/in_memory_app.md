Module qyver.framework.dsl.app.in_memory.in_memory_app
============================================================

Classes
-------

`InMemoryApp(sources: Sequence[qyver.framework.dsl.source.in_memory_source.InMemorySource], indices: Sequence[qyver.framework.dsl.index.index.Index], vector_database: qyver.framework.dsl.storage.vector_database.VectorDatabase | None, context: qyver.framework.common.dag.context.ExecutionContext)`
:   In-memory implementation of the App class.
    
    Initialize the InMemoryApp from an InMemoryExecutor.
    Args:
        sources (list[InMemorySource]): List of in-memory sources.
        indices (list[Index]): List of indices.
        vector_database (VectorDatabase | None): Vector database instance. Defaults to InMemory.
        context (Mapping[str, Mapping[str, Any]]): Context mapping.

    ### Ancestors (in MRO)

    * qyver.framework.dsl.app.interactive.interactive_app.InteractiveApp
    * qyver.framework.dsl.app.online.online_app.OnlineApp
    * qyver.framework.dsl.app.app.App
    * abc.ABC
    * typing.Generic
    * qyver.framework.dsl.query.query_mixin.QueryMixin
