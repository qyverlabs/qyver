Module qyver.framework.dsl.index.util.effect_with_referenced_schema_object
================================================================================

Classes
-------

`EffectWithReferencedSchemaObject(base_effect: Effect[AggregationInputT, EmbeddingInputT], resolved_affected_schema_reference: ResolvedSchemaReference, resolved_affecting_schema_reference: ResolvedSchemaReference, event_schema: EventSchemaObject)`
:   EffectWithReferencedSchemaObject(base_effect: 'Effect[AggregationInputT, EmbeddingInputT]', resolved_affected_schema_reference: 'ResolvedSchemaReference', resolved_affecting_schema_reference: 'ResolvedSchemaReference', event_schema: 'EventSchemaObject')

    ### Ancestors (in MRO)

    * typing.Generic

    ### Class variables

    `base_effect: qyver.framework.dsl.index.effect.Effect[~AggregationInputT, ~EmbeddingInputT]`
    :

    `event_schema: qyver.framework.common.schema.event_schema_object.EventSchemaObject`
    :

    `resolved_affected_schema_reference: qyver.framework.common.dag.resolved_schema_reference.ResolvedSchemaReference`
    :

    `resolved_affecting_schema_reference: qyver.framework.common.dag.resolved_schema_reference.ResolvedSchemaReference`
    :

    ### Static methods

    `from_base_effect(base_effect: Effect, schemas: set[SchemaObject]) ‑> qyver.framework.dsl.index.util.effect_with_referenced_schema_object.EffectWithReferencedSchemaObject`
    :

    ### Instance variables

    `dag_effect: DagEffect`
    :
