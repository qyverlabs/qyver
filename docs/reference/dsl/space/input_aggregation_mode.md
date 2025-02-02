Module qyver.framework.dsl.space.input_aggregation_mode
=============================================================

Classes
-------

`InputAggregationMode(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access::
    
    >>> Color.RED
    <Color.RED: 1>
    
    - value lookup:
    
    >>> Color(1)
    <Color.RED: 1>
    
    - name lookup:
    
    >>> Color['RED']
    <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `INPUT_AVERAGE`
    :

    `INPUT_MAXIMUM`
    :

    `INPUT_MINIMUM`
    :
