Module qyver.framework.dsl.query.query
============================================

Classes
-------

`Query(index: qyver.framework.dsl.index.index.Index, weights: collections.abc.Mapping[qyver.framework.dsl.space.space.Space, float | int | qyver.framework.dsl.query.param.Param] | None = None)`
:   A class representing a query. Build queries using Params as placeholders for weights or query text,
    and supply their value later on when executing a query.
    
    Attributes:
        index (Index): The index to be used for the query.
        weights (Mapping[Space, NumericParamType] | None, optional): The mapping of spaces to weights.
            Defaults to None, which is equal weight for each space.
    
    Initialize the Query.
    
    Args:
        index (Index): The index to be used for the query.
        weights (Mapping[Space, NumericParamType] | None, optional): The mapping of spaces to weights.
            Defaults to None, which is equal weight for each space.

    ### Methods

    `find(self, schema: qyver.framework.common.schema.id_schema_object.IdSchemaObject) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Find a schema in the query.
        
        Args:
            schema (IdSchemaObject): The schema to find.
        
        Returns:
            QueryDescriptor: The QueryDescriptor object.
        
        Raises:
            QueryException: If the index does not have the queried schema.
