Module qyver.framework.dsl.executor.executor
==================================================

Classes
-------

`Executor(sources: ~SourceT | Sequence[~SourceT], indices: qyver.framework.dsl.index.index.Index | typing.Annotated[Sequence[qyver.framework.dsl.index.index.Index], beartype.vale.Is[TypeValidator.list_validator.validator]], vector_database: qyver.framework.dsl.storage.vector_database.VectorDatabase, context: qyver.framework.common.dag.context.ExecutionContext)`
:   Abstract base class for an executor.
    
    Initialize the Executor.
    Args:
        sources (list[SourceT]): The list of sources.
        indices (list[Index]): The list of indices.
        vector_database (VectorDatabase): The vector database which the executor will use.
        context (Mapping[str, Mapping[str, Any]]): The context mapping.

    ### Ancestors (in MRO)

    * abc.ABC
    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.executor.interactive.interactive_executor.InteractiveExecutor
    * qyver.framework.dsl.executor.rest.rest_executor.RestExecutor

    ### Methods

    `run(self) ‑> qyver.framework.dsl.app.app.App`
    :   Abstract method to run the executor.
        Returns:
            App: An instance of App.
