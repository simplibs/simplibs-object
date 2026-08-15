from .validate_default_is_defined import validate_default_is_defined
from .validate_default_matches_annotation import validate_default_matches_annotation
from .raise_default_is_defined_in_composition import raise_default_is_defined_in_composition


_DESIGN_NOTES = """
# Default Processing Validations Package

## Purpose
Aggregates and exposes the core structural and type-safety validation functions used during the initialization processing of default values.

## Internal Components Registry

| Component                            | Type     | Description                                                                          |
| :----------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_default_is_defined`         | Function | Verifies that a constant leaf node explicitly declares its mandatory default value.   |
| `validate_default_matches_annotation` | Function | Validates that the assigned default value strictly conforms to the compiled type.     |
| `raise_default_is_defined_in_composition` | Function | Enforces architectural boundaries by rejecting explicit default attributes on compound objects. |
"""