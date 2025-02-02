Module qyver.framework.dsl.index.effect
=============================================

Classes
-------

`Effect(space: qyver.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT], affected_schema_reference: qyver.framework.common.schema.event_schema_object.SchemaReference, affecting_schema_reference: qyver.framework.common.schema.event_schema_object.SchemaReference | qyver.framework.common.schema.event_schema_object.MultipliedSchemaReference, filter_: qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField])`
:   An effect represents a conditional interaction within a `Space` where the
    `affecting_schema_reference` interacted with the `affected_schema_reference`.
    
    It allows you to real-time adjust embeddings based on interaction.
    e.g.: A `User` schema interacts with a `Post` schema, if `event.type == 'like'.

    ### Ancestors (in MRO)

    * typing.Generic

    ### Class variables

    `affected_schema_reference: qyver.framework.common.schema.event_schema_object.SchemaReference`
    :

    `affecting_schema_reference: qyver.framework.common.schema.event_schema_object.SchemaReference | qyver.framework.common.schema.event_schema_object.MultipliedSchemaReference`
    :

    `filter_: qyver.framework.common.interface.comparison_operand.ComparisonOperation[qyver.framework.common.schema.schema_object.SchemaField]`
    :

    `space: qyver.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT]`
    :
