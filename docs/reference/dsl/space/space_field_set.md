Module qyver.framework.dsl.space.space_field_set
======================================================

Classes
-------

`SpaceFieldSet(space: qyver.framework.dsl.space.space.Space, fields: set[qyver.framework.common.schema.schema_object.SchemaField])`
:   A class representing a set of fields in a space.
    Attributes:
        space (Space): The space.
        fields (set[SchemaField]): The set of fields.

    ### Ancestors (in MRO)

    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.space.image_space_field_set.ImageDescriptionSpaceFieldSet
    * qyver.framework.dsl.space.image_space_field_set.ImageSpaceFieldSet

    ### Class variables

    `fields: set[qyver.framework.common.schema.schema_object.SchemaField]`
    :

    `space: qyver.framework.dsl.space.space.Space`
    :

    ### Instance variables

    `field_names_text: Sequence[str]`
    :

    `fields_id: str`
    :

    `input_type: type[~SIT]`
    :

    ### Methods

    `get_field_for_schema(self, schema_: Any) ‑> qyver.framework.common.schema.schema_object.SchemaField | None`
    :
