Module qyver.framework.dsl.query.predicate.binary_predicate
=================================================================

Classes
-------

`LooksLikePredicate(left_param: qyver.framework.common.schema.schema_object.SchemaField, right_param: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None] | qyver.framework.dsl.query.param.Param, weight: float | int | qyver.framework.dsl.query.param.Param)`
:   QueryPredicate(op: ~OPT, params: list[qyver.framework.common.schema.schema_object.SchemaField | qyver.framework.dsl.query.param.Param | collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | None | tuple[str | None, str | None]], weight_param: float | int | qyver.framework.dsl.query.param.Param)

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.predicate.binary_predicate.BinaryPredicate
    * qyver.framework.dsl.query.predicate.query_predicate.QueryPredicate
    * typing.Generic

`SimilarPredicate(left_param: qyver.framework.common.schema.schema_object.SchemaField, right_param: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None] | qyver.framework.dsl.query.param.Param, weight: float | int | qyver.framework.dsl.query.param.Param, left_param_node: qyver.framework.common.dag.node.Node)`
:   QueryPredicate(op: ~OPT, params: list[qyver.framework.common.schema.schema_object.SchemaField | qyver.framework.dsl.query.param.Param | collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | None | tuple[str | None, str | None]], weight_param: float | int | qyver.framework.dsl.query.param.Param)

    ### Ancestors (in MRO)

    * qyver.framework.dsl.query.predicate.binary_predicate.BinaryPredicate
    * qyver.framework.dsl.query.predicate.query_predicate.QueryPredicate
    * typing.Generic
