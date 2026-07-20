from .validate_type_from_tuple_is_not_none import validate_type_from_tuple_is_not_none
from .validate_type_tuple_is_not_nested import validate_type_tuple_is_not_nested


_DESIGN_NOTES = """
# Tuple Type Validation Sub-Package

## Purpose
Houses deep structural validation filters that verify the internal elements of a standard Python tuple when used to define multiple allowed types.

## Internal Components Registry

| Component                             | Type     | Description                                                                          |
| :------------------------------------ | :------- | :----------------------------------------------------------------------------------- |
| `validate_type_from_tuple_is_not_none`| Function | Rejects literal 'None' values embedded inside the type collection sequence.          |
| `validate_type_tuple_is_not_nested`   | Function | Enforces a flat layout by blocking any sub-tuples inside the main type definition.   |
"""