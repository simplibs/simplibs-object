from .raise_validate_type_is_not_valid import raise_validate_type_is_not_valid
from .validate_type_is_defined import validate_type_is_defined
from .validate_type_is_not_empty import validate_type_is_not_empty
from .validate_type_is_not_none import validate_type_is_not_none


_DESIGN_NOTES = """
# Base Type Validation Sub-Package

## Purpose
Provides critical high-level entry guards and fallbacks ensuring the primary presence, population, and structural evaluation of the raw `_type` attribute.

## Internal Components Registry

| Component                          | Type     | Description                                                                          |
| :--------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_type_is_defined`         | Function | Verifies that the attribute is present on the blueprint and not left at UNSET.       |
| `validate_type_is_not_none`        | Function | Blocks assigning the literal None singleton directly as a type bound.                |
| `validate_type_is_not_empty`        | Function | Rejects empty structures or collections that evaluate to falsy states.               |
| `raise_validate_type_is_not_valid`  | Function | Terminal catch-all fallback that raises a domain exception for unrecognized inputs.  |
"""