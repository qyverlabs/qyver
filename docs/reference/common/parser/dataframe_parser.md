Module qyver.framework.common.parser.dataframe_parser
===========================================================

Classes
-------

`DataFrameParser(schema: IdSchemaObjectT, mapping: Mapping[SchemaField, str] | None = None)`
:   DataFrameParser gets a `pd.DataFrame` and using column-string mapping
    it transforms the `DataFrame` to a desired schema.
    
    Initialize DataParser
    
    Get the desired output schema and initialize a default mapping
    that can be extended by DataParser realizations.
    
    Args:
        schema (IdSchemaObjectT): SchemaObject describing the desired output.
        mapping (Mapping[SchemaField, str], optional): Realizations can use the `SchemaField` to `str` mapping
            to define their custom mapping logic.
    
    Raises:
        InitializationException: Parameter `schema` is of invalid type.

    ### Ancestors (in MRO)

    * qyver.framework.common.parser.data_parser.DataParser
    * abc.ABC
    * typing.Generic

    ### Methods

    `unmarshal(self, data: pd.DataFrame) ‑> list[qyver.framework.common.parser.parsed_schema.ParsedSchema]`
    :   Parses the given DataFrame into a list of ParsedSchema objects according to the defined schema and mapping.
        Args:
            data (pd.DataFrame): Pandas DataFrame input.
        Returns:
            list[ParsedSchema]: A list of ParsedSchema objects that will be processed by the spaces.
