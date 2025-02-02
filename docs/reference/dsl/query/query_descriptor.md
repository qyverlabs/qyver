Module qyver.framework.dsl.query.query_descriptor
=======================================================

Classes
-------

`QueryDescriptor(index: qyver.framework.dsl.index.index.Index, schema: qyver.framework.common.schema.id_schema_object.IdSchemaObject, clauses: collections.abc.Sequence[qyver.framework.dsl.query.query_clause.QueryClause] | None = None)`
:   A class representing a query object. Use .with_vector to run queries using a stored
    vector, or use .similar for queries where you supply the query at query-time. Or combine
    them, or even combine multiple .similar to supply different queries for each space in the
    Index.

    ### Instance variables

    `clauses: Sequence[qyver.framework.dsl.query.query_clause.QueryClause]`
    :

    `index: qyver.framework.dsl.index.index.Index`
    :

    `schema: qyver.framework.common.schema.id_schema_object.IdSchemaObject`
    :

    ### Methods

    `append_missing_mandatory_clauses(self) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :

    `filter(self, comparison_operation: qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField] | qyver.framework.common.interface.comparison_operand._Or) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Add a 'filter' clause to the query. This filters the results from the db
        to only contain items based on the filtering input.
        E.g:
        filter(color_schema.color == "blue")
        filter(color_schema.color == Param("color_param"))
        filter(color_schema.color != "red")
        filter(color_schema.rating > 3)
        filter(color_schema.rating >= 3)
        filter(color_schema.rating < 3)
        filter(color_schema.rating <= 3)
        filter((color_schema.color == "blue") | (color_schema.color == "red"))
        filter(color_schema.categories.contains(["bright", "matte"]))
            - returns both bright and matte colors
        filter(color_schema.categories.not_contains(["bright", "matte"]))
            - returns colors that are non-bright and non-matte
        filter(color_schema.categories.contains_all(["bright", "blue"]))
            - returns colors that are bright and blue at the same time
        Args:
            comparison_operation ComparisonOperation[SchemaField]: The comparison operation.
        
        Returns:
            Self: The query object itself.

    `get_clause_by_type(self, clause_type: type[~QueryClauseT]) ‑> ~QueryClauseT | None`
    :

    `get_clauses_by_type(self, clause_type: type[~QueryClauseT]) ‑> list[~QueryClauseT]`
    :

    `get_context_time(self, default: int | typing.Any) ‑> int`
    :

    `get_hard_filters(self) ‑> list[qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField]]`
    :

    `get_limit(self) ‑> int`
    :

    `get_looks_like_filter(self) ‑> qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.LooksLikePredicate] | None`
    :

    `get_mandatory_clause_by_type(self, clause_type: type[~QueryClauseT]) ‑> ~QueryClauseT`
    :

    `get_param_value_to_set_for_unset_space_weight_clauses(self) ‑> dict[str, float]`
    :

    `get_radius(self) ‑> float | None`
    :

    `get_selected_fields(self) ‑> Sequence[qyver.framework.common.schema.schema_object.SchemaField]`
    :

    `get_similar_filters_spaces(self) ‑> list[qyver.framework.dsl.space.space.Space]`
    :

    `get_weighted_clauses(self) ‑> list[qyver.framework.dsl.query.query_clause.WeightedQueryClause]`
    :

    `get_weights_by_space(self) ‑> dict[qyver.framework.dsl.space.space.Space, float]`
    :

    `limit(self, limit: int | qyver.framework.dsl.query.param.Param | None) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Set a limit to the number of results returned by the query.
        If the limit is None, -1 will be used, which is not handled by all databases.
        
        Args:
            limit (IntParamType): The maximum number of results to return.
        Returns:
            Self: The query object itself.

    `nlq_suggestions(self, feedback: str | None = None) ‑> qyver.framework.dsl.query.nlq.suggestion.query_suggestion_model.QuerySuggestionsModel`
    :   Get suggestions for improving the natural language query parameters.
        
        This method analyzes the current query parameters and provides suggestions for improvement,
        including parameter naming, clarity, and overall query structure improvements.
        It requires that a natural language query has been set using with_natural_query().
        
        Args:
            feedback (str | None, optional): Additional feedback from the query creator to help
                generate more targeted suggestions. For example, you might provide context about
                specific requirements or constraints. Defaults to None.
        
        Returns:
            QuerySuggestionsModel: A model containing improvement suggestions and clarifying questions.
                You can access the suggestions directly via the model's attributes or call
                .print() for a formatted display of the suggestions.
        
                Example usage:
                ```python
                suggestions = query.nlq_suggestions()
                suggestions.print()  # Prints formatted suggestions
                # Or access directly:
                print(suggestions.improvement_suggestions)
                print(suggestions.clarifying_questions)
                ```
        
        Raises:
            QueryException: If with_natural_query() has not been called before this method.

    `override_now(self, now: int | qyver.framework.dsl.query.param.Param) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :

    `radius(self, radius: float | int | qyver.framework.dsl.query.param.Param | None) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Set a radius for the search in the query. The radius is a float value that
        determines the maximum distance to the input vector in the search.
        A lower radius value means that the enforced maximum distance is lower,
        therefore closer vectors are returned only.
        A radius of 0.05 means the lowest cosine similarity of items returned to the query vector is 0.95.
        The valid range is between 0 and 1. Otherwise it will raise ValueError.
        
        Args:
            radius (NumericParamType | None): The maximum distance of the returned items from the query vector.
            If None, all results are returned.
        
        Returns:
            Self: The query object itself.
        
        Raises:
            ValueError: If the radius is not between 0 and 1.

    `replace_clauses(self, clauses: Sequence[qyver.framework.dsl.query.query_clause.QueryClause]) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :

    `select(self, *fields: qyver.framework.common.schema.schema_object.SchemaField | str | qyver.framework.dsl.query.param.Param) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Select specific fields from the schema to be returned in the query results.
        
        Args:
            *fields (SchemaField | str | Param): The fields to select. Can be:
                - One or more SchemaField objects
                - One or more field names as strings
                - A single Param object that will be filled with fields later
                If no fields are provided, returns an empty selection.
        
        Returns:
            Self: The query object itself.
        
        Raises:
            QueryException: If multiple Param objects are provided or Param is mixed with other field types.
            TypeException: If any of the fields are of unsupported types.
            FieldException: If any of the schema fields are not part of the schema.

    `select_all(self) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Select all fields from the schema to be returned in the query results.
        
        Returns:
            Self: The query object itself.

    `similar(self, space_field_set: qyver.framework.dsl.space.has_space_field_set.HasSpaceFieldSet | qyver.framework.dsl.space.space_field_set.SpaceFieldSet, param: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None] | qyver.framework.dsl.query.param.Param, weight: float | int | qyver.framework.dsl.query.param.Param = 1.0) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Add a 'similar' clause to the query. Similar queries compile query inputs (like query text) into vectors
        using a space and then use the query_vector (weighted with weight param) to search
        in the referenced space of the index.
        
        Args:
            space_field_set (HasSpaceFieldSet | SpaceFieldSet): The space or field set to search within.
            param (ParamType): The parameter. Basically the query itself. It can be a fixed value,
            or a placeholder (Param) for later substitution.
            weight (NumericParamType, optional): The weight. Defaults to 1.0.
        
        Returns:
            Self: The query object itself.
        
        Raises:
            QueryException: If the space is already bound in the query.
            InvalidSchemaException: If the schema is not in the similarity field's schema types.

    `space_weights(self, weight_by_space: Mapping[qyver.framework.dsl.space.space.Space, float | int | qyver.framework.dsl.query.param.Param]) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :

    `with_natural_query(self, natural_query: str | qyver.framework.dsl.query.param.Param, client_config: qyver.framework.common.nlq.open_ai.OpenAIClientConfig, system_prompt: str | qyver.framework.dsl.query.param.Param | None = None) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Sets a natural language query based on which empty Params will have values set.
        
        Args:
            natural_query (StringParamType): Query containing desired characteristics.
            client_config (OpenAIClientConfig): Client config to initialize the client with.
            system_prompt (StringParamType | None): Custom system prompt to use for the query. Defaults to None.
        Returns:
            Self: The query object itself.

    `with_vector(self, schema_obj: qyver.framework.common.schema.id_schema_object.IdSchemaObject, id_param: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None] | qyver.framework.dsl.query.param.Param, weight: float | int | qyver.framework.dsl.query.param.Param = 1.0) ‑> qyver.framework.dsl.query.query_descriptor.QueryDescriptor`
    :   Add a 'with_vector' clause to the query. This fetches an object with id_param
        from the db and uses the vector of that item for search purposes. Weighting
        happens at the space level (and if there is also a .similar query present,
        this part has weight=1 compared to the weight set at .similar for the query
        vector).
        
        Args:
            weight (NumericParamType): Weight attributed to the vector retrieved via this clause in the aggregated
                query.
            schema_obj (SchemaObject | T): The schema object the vector is originating from.
            id_param (ParamType): The ID parameter. Eventually it is the ID of the vector to be used in the query.
        
        Returns:
            Self: The query object itself.

`QueryDescriptorValidator()`
:   

    ### Static methods

    `validate(query_descriptor: QueryDescriptor) ‑> None`
    :
