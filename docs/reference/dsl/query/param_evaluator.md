Module qyver.framework.dsl.query.param_evaluator
======================================================

Classes
-------

`EvaluatedParamInfo(limit: int, radius: float | None, space_weight_map: dict[qyver.framework.dsl.space.space.Space, float], hard_filters: list[qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField]], similar_filters: dict[qyver.framework.dsl.space.space.Space, list[qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.SimilarPredicate]]], looks_like_filter: Optional[qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.LooksLikePredicate]], natural_language_query_params: qyver.framework.dsl.query.natural_language_query_param_handler.NaturalLanguageQueryParams)`
:   EvaluatedParamInfo(limit: int, radius: float | None, space_weight_map: dict[qyver.framework.dsl.space.space.Space, float], hard_filters: list[qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField]], similar_filters: dict[qyver.framework.dsl.space.space.Space, list[qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.SimilarPredicate]]], looks_like_filter: Optional[qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.LooksLikePredicate]], natural_language_query_params: qyver.framework.dsl.query.natural_language_query_param_handler.NaturalLanguageQueryParams)

    ### Class variables

    `hard_filters: list[qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField]]`
    :

    `limit: int`
    :

    `looks_like_filter: Optional[qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.LooksLikePredicate]]`
    :

    `natural_language_query_params: qyver.framework.dsl.query.natural_language_query_param_handler.NaturalLanguageQueryParams`
    :

    `radius: float | None`
    :

    `similar_filters: dict[qyver.framework.dsl.space.space.Space, list[qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.SimilarPredicate]]]`
    :

    `space_weight_map: dict[qyver.framework.dsl.space.space.Space, float]`
    :
