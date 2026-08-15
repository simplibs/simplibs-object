from .validate_type_is_defined import validate_type_is_defined
from .validate_type_is_not_none import validate_type_is_not_none
from .validate_type_is_not_empty import validate_type_is_not_empty
from .raise_validate_type_is_not_valid import raise_validate_type_is_not_valid
from .validate_type_from_tuple_is_not_none import validate_type_from_tuple_is_not_none
from .validate_type_tuple_is_not_nested import validate_type_tuple_is_not_nested
from .raise_union_type_contain_none import raise_union_type_contain_none


_DESIGN_NOTES = """
# Type Validation Sub-Package

## Purpose
Provides all validation filters and structured error generators used to verify
the `_type` attribute of Simple classes. Ensures correctness of type definitions,
tuple layouts, and union semantics.

## Internal Components Registry

| Component                             | Type     | Description                                                                |
| :------------------------------------ | :------- | :------------------------------------------------------------------------- |
| `validate_type_is_defined`            | Function | Ensures `_type` is explicitly declared and not UNSET.                      |
| `validate_type_is_not_none`           | Function | Blocks using literal `None` as a type definition.                          |
| `validate_type_is_not_empty`          | Function | Rejects empty or falsy type declarations.                                  |
| `raise_validate_type_is_not_valid`    | Function | Fallback error for unrecognized or invalid type inputs.                    |
| `validate_type_from_tuple_is_not_none`| Function | Rejects `None` values inside tuple-based type definitions.                 |
| `validate_type_tuple_is_not_nested`   | Function | Enforces flat tuple structure for multi-type definitions.                  |
| `raise_union_type_contain_none`       | Function | Raises error when a union type contains `NoneType`.                        |
"""
