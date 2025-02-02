Module qyver.framework.dsl.index.util.event_aggregation_effect_group
==========================================================================

Classes
-------

`EventAggregationEffectGroup(key: GroupKey[AggregationInputT, EmbeddingInputT], effects: Sequence[EffectWithReferencedSchemaObject])`
:   Group of effects with the same space, event schema, affected schema and affecting schema.

    ### Ancestors (in MRO)

    * typing.Generic

    ### Class variables

    `effects: Sequence[qyver.framework.dsl.index.util.effect_with_referenced_schema_object.EffectWithReferencedSchemaObject]`
    :

    `key: qyver.framework.dsl.index.util.event_aggregation_effect_group.GroupKey[~AggregationInputT, ~EmbeddingInputT]`
    :

    ### Static methods

    `group_by_event_and_affecting_schema(effects: Sequence[EffectWithReferencedSchemaObject[AggregationInputT, EmbeddingInputT]]) ‑> list[qyver.framework.dsl.index.util.event_aggregation_effect_group.EventAggregationEffectGroup[~AggregationInputT, ~EmbeddingInputT]]`
    :

`GroupKey(space: Space[AggregationInputT, EmbeddingInputT], event_schema: EventSchemaObject, resolved_affected_schema_reference: ResolvedSchemaReference, resolved_affecting_schema: IdSchemaObject, resolved_affecting_reference_field: SchemaReference)`
:   GroupKey(space: 'Space[AggregationInputT, EmbeddingInputT]', event_schema: 'EventSchemaObject', resolved_affected_schema_reference: 'ResolvedSchemaReference', resolved_affecting_schema: 'IdSchemaObject', resolved_affecting_reference_field: 'SchemaReference')

    ### Ancestors (in MRO)

    * typing.Generic

    ### Class variables

    `event_schema: qyver.framework.common.schema.event_schema_object.EventSchemaObject`
    :

    `resolved_affected_schema_reference: qyver.framework.common.dag.resolved_schema_reference.ResolvedSchemaReference`
    :

    `resolved_affecting_reference_field: qyver.framework.common.schema.event_schema_object.SchemaReference`
    :

    `resolved_affecting_schema: qyver.framework.common.schema.id_schema_object.IdSchemaObject`
    :

    `space: qyver.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT]`
    :
