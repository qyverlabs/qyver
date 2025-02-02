Module qyver.framework.dsl.executor.query.query_executor
==============================================================

Classes
-------

`QueryExecutor(app: qyver.framework.dsl.app.app.App, query_descriptor: qyver.framework.dsl.query.query_descriptor.QueryDescriptor, query_vector_factory: qyver.framework.dsl.query.query_vector_factory.QueryVectorFactory)`
:   QueryExecutor provides an interface to execute predefined queries with query time parameters.
    
    Initializes the QueryExecutor.
    
    Args:
        app: An instance of the App class.
        query_descriptor: An instance of the QueryDescriptor class representing the query to be executed.
        evaluator: An instance of the QueryDagEvaluator class used to evaluate the query.

    ### Methods

    `calculate_query_node_inputs_by_node_id(self, query_descriptor: qyver.framework.dsl.query.query_descriptor.QueryDescriptor) ‑> dict[str, list[qyver.framework.query.query_node_input.QueryNodeInput]]`
    :

    `query(self, **params: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None]) ‑> qyver.framework.dsl.query.result.QueryResult`
    :   Execute a query with keyword parameters.
        
        Args:
            **params: Arbitrary arguments with keys corresponding to the `name` attribute of the `Param` instance.
        
        Returns:
            Result: The result of the query execution that can be inspected and post-processed.
        
        Raises:
            QueryException: If the query index is not amongst the executor's indices.
