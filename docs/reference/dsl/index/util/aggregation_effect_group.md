Module qyver.framework.dsl.index.util.aggregation_effect_group
====================================================================

Classes
-------

`AggregationEffectGroup(space: Space[AggregationInputT, EmbeddingInputT], affected_schema: SchemaObject, effects: Sequence[EffectWithReferencedSchemaObject[AggregationInputT, EmbeddingInputT]])`
:   Group of effects with the same space and affected schema.

    ### Ancestors (in MRO)

    * typing.Generic

    ### Class variables

    `affected_schema: qyver.framework.common.schema.schema_object.SchemaObject`
    :

    `effects: Sequence[qyver.framework.dsl.index.util.effect_with_referenced_schema_object.EffectWithReferencedSchemaObject[~AggregationInputT, ~EmbeddingInputT]]`
    :

    `space: qyver.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT]`
    :

    ### Static methods

    `from_filtered_effects(filtered_effects: Sequence[EffectWithReferencedSchemaObject[AggregationInputT, EmbeddingInputT]]) ‑> qyver.framework.dsl.index.util.aggregation_effect_group.AggregationEffectGroup[~AggregationInputT, ~EmbeddingInputT]`
    :
