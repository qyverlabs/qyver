Module qyver.framework.dsl.query.nlq.nlq_handler
======================================================

Classes
-------

`NLQHandler()`
:   

    ### Static methods

    `fill_params(natural_query: str, query_clauses: Sequence[qyver.framework.dsl.query.query_clause.QueryClause], client_config: qyver.framework.common.nlq.open_ai.OpenAIClientConfig, system_prompt: str | None = None) ‑> dict[str, typing.Any]`
    :

    `suggest_improvements(query_clauses: Sequence[qyver.framework.dsl.query.query_clause.QueryClause], natural_query: str | None, feedback: str | None, client_config: qyver.framework.common.nlq.open_ai.OpenAIClientConfig, system_prompt: str | None = None) ‑> qyver.framework.dsl.query.nlq.suggestion.query_suggestion_model.QuerySuggestionsModel`
    :
