Module qyver.framework.dsl.query.query_clause
===================================================

Classes
-------

`HardFilterClause(value_param: Param | Evaluated[Param], op: ComparisonOperationType, operand: SchemaField, group_key: int | None)`
:   HardFilterClause(value_param: 'Param | Evaluated[Param]', op: 'ComparisonOperationType', operand: 'SchemaField', group_key: 'int | None')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * abc.ABC

    ### Class variables

    `group_key: int | None`
    :

    `op: qyver.framework.common.interface.comparison_operation_type.ComparisonOperationType`
    :

    `operand: qyver.framework.common.schema.schema_object.SchemaField`
    :

    ### Instance variables

    `annotation: str`
    :

    `value_accepted_type: type`
    :

    ### Methods

    `evaluate(self) ‑> qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField] | None`
    :

    `get_default_value_param_name(self) ‑> str`
    :

`LimitClause(value_param: Param | Evaluated[Param])`
:   LimitClause(value_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Methods

    `evaluate(self) ‑> int`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_value(self) ‑> int`
    :

`LooksLikeFilterClause(value_param: Param | Evaluated[Param], weight_param: Param | Evaluated[Param], schema_field: SchemaField)`
:   LooksLikeFilterClause(value_param: 'Param | Evaluated[Param]', weight_param: 'Param | Evaluated[Param]', schema_field: 'SchemaField')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.WeightedQueryClause
    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * abc.ABC

    ### Class variables

    `schema_field: qyver.framework.common.schema.schema_object.SchemaField`
    :

    ### Instance variables

    `annotation: str`
    :

    `value_accepted_type: type`
    :

    ### Methods

    `evaluate(self) ‑> qyver.framework.dsl.query.predicate.binary_predicate.EvaluatedBinaryPredicate[qyver.framework.dsl.query.predicate.binary_predicate.LooksLikePredicate] | None`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_default_weight_param_name(self) ‑> str`
    :

`NLQClause(value_param: Param | Evaluated[Param], client_config: OpenAIClientConfig)`
:   NLQClause(value_param: 'Param | Evaluated[Param]', client_config: 'OpenAIClientConfig')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Class variables

    `client_config: qyver.framework.common.nlq.open_ai.OpenAIClientConfig`
    :

    ### Methods

    `evaluate(self) ‑> str | None`
    :

    `get_default_value_param_name(self) ‑> str`
    :

`NLQSystemPromptClause(value_param: Param | Evaluated[Param])`
:   NLQSystemPromptClause(value_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Methods

    `evaluate(self) ‑> str | None`
    :

    `get_default_value_param_name(self) ‑> str`
    :

`OverriddenNowClause(value_param: Param | Evaluated[Param])`
:   OverriddenNowClause(value_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Methods

    `evaluate(self) ‑> int | None`
    :

    `get_default_value_param_name(self) ‑> str`
    :

`QueryClause(value_param: Param | Evaluated[Param])`
:   QueryClause(value_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.query.query_clause.HardFilterClause
    * qyver.framework.dsl.query.query_clause.LimitClause
    * qyver.framework.dsl.query.query_clause.NLQClause
    * qyver.framework.dsl.query.query_clause.NLQSystemPromptClause
    * qyver.framework.dsl.query.query_clause.OverriddenNowClause
    * qyver.framework.dsl.query.query_clause.RadiusClause
    * qyver.framework.dsl.query.query_clause.SelectClause
    * qyver.framework.dsl.query.query_clause.SpaceWeightClause
    * qyver.framework.dsl.query.query_clause.WeightedQueryClause

    ### Class variables

    `value_param: qyver.framework.dsl.query.param.Param | qyver.framework.common.interface.evaluated.Evaluated[qyver.framework.dsl.query.param.Param]`
    :

    ### Static methods

    `get_param(param: Param | Evaluated[Param]) ‑> qyver.framework.dsl.query.param.Param`
    :

    `get_param_value(param: Param | Evaluated[Param]) ‑> collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None]`
    :

    ### Instance variables

    `params: Sequence[Param | Evaluated[Param]]`
    :

    `value_accepted_type: type`
    :

    `value_param_name: str`
    :

    ### Methods

    `alter_value(self, params: Mapping[str, ParamInputType], is_override_set: bool) ‑> Self`
    :

    `evaluate(self) ‑> ~EvaluatedQueryT`
    :

    `get_allowed_values(self, param: Param | Evaluated[Param]) ‑> set[collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None]]`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_value(self) ‑> float | int | str | qyver.framework.common.data_types.Vector | list[float] | list[str] | qyver.framework.common.schema.blob_information.BlobInformation | None`
    :

`RadiusClause(value_param: Param | Evaluated[Param])`
:   RadiusClause(value_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Methods

    `evaluate(self) ‑> float | None`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_value(self) ‑> float | None`
    :

`SelectClause(value_param: Param | Evaluated[Param])`
:   SelectClause(value_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Methods

    `evaluate(self) ‑> list[str]`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_value(self) ‑> list[str]`
    :

`SimilarFilterClause(value_param: Param | Evaluated[Param], weight_param: Param | Evaluated[Param], field_set: SpaceFieldSet)`
:   SimilarFilterClause(value_param: 'Param | Evaluated[Param]', weight_param: 'Param | Evaluated[Param]', field_set: 'SpaceFieldSet')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.WeightedQueryClause
    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * abc.ABC

    ### Class variables

    `field_set: qyver.framework.dsl.space.space_field_set.SpaceFieldSet`
    :

    ### Instance variables

    `annotation: str`
    :

    `space: Space`
    :

    `value_accepted_type: type`
    :

    ### Methods

    `evaluate(self) ‑> tuple[qyver.framework.dsl.space.space.Space, qyver.framework.common.interface.weighted.Weighted[float | int | str | qyver.framework.common.data_types.Vector | list[float] | list[str] | qyver.framework.common.schema.blob_information.BlobInformation]] | None`
    :

    `get_allowed_values(self, param: Param | Evaluated[Param]) ‑> set[collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None]]`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_default_weight_param_name(self) ‑> str`
    :

`SpaceWeightClause(value_param: Param | Evaluated[Param], space: Space)`
:   SpaceWeightClause(value_param: 'Param | Evaluated[Param]', space: 'Space')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic
    * qyver.framework.common.interface.has_annotation.HasAnnotation
    * abc.ABC

    ### Class variables

    `space: qyver.framework.dsl.space.space.Space`
    :

    ### Instance variables

    `annotation: str`
    :

    `value_accepted_type: type`
    :

    ### Methods

    `evaluate(self) ‑> tuple[qyver.framework.dsl.space.space.Space, float]`
    :

    `get_default_value_param_name(self) ‑> str`
    :

    `get_value(self) ‑> float`
    :

`WeightedQueryClause(value_param: Param | Evaluated[Param], weight_param: Param | Evaluated[Param])`
:   WeightedQueryClause(value_param: 'Param | Evaluated[Param]', weight_param: 'Param | Evaluated[Param]')

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.query_clause.QueryClause
    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.query.query_clause.LooksLikeFilterClause
    * qyver.framework.dsl.query.query_clause.SimilarFilterClause

    ### Class variables

    `weight_param: qyver.framework.dsl.query.param.Param | qyver.framework.common.interface.evaluated.Evaluated[qyver.framework.dsl.query.param.Param]`
    :

    ### Instance variables

    `params: Sequence[Param | Evaluated[Param]]`
    :

    `weight_accepted_type: type`
    :

    `weight_param_name: str`
    :

    ### Methods

    `alter_weight(self, params: Mapping[str, ParamInputType], is_override_set: bool) ‑> Self`
    :

    `get_default_weight_param_name(self) ‑> str`
    :

    `get_weight(self) ‑> float`
    :
