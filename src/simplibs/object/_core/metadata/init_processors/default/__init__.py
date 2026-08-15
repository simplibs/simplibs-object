from .process_default_for_constant import process_default_for_constant
from .validations import raise_default_is_defined_in_composition


_DESIGN_NOTES = """
# Attribute Default Processing Package

## Purpose
Coordinates the metadata processing routines responsible for extracting, validating, and locking the fallback default boundaries for both constant leaf nodes and composite models.

## Internal Components Registry

| Component                                 | Type     | Description                                                                          |
| :---------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `process_default_for_constant`           | Function | The primary pipeline entrypoint that extracts and ensures type compliance of constant defaults. |
| `raise_default_is_defined_in_composition` | Function | Enforces architectural boundaries by rejecting explicit default attributes on compound objects. |
"""