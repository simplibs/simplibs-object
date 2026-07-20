from .validate_inners_is_defined import validate_inners_is_defined
from .validate_inners_is_not_empty import validate_inners_is_not_empty
from .validate_inners_is_tuple import validate_inners_is_tuple


_DESIGN_NOTES = """
# Inners Container Validation Sub-Package

## Purpose
Houses high-level structural integrity filters evaluated against the master `_inners` attribute collection as a whole.

## Internal Components Registry

| Component                             | Type     | Description                                                                          |
| :------------------------------------ | :------- | :----------------------------------------------------------------------------------- |
| `validate_inners_is_defined`          | Function | Verifies that the `_inners` attribute token is actively present on the target class. |
| `validate_inners_is_not_empty`        | Function | Rejects empty tuple layouts, forcing atomic nodes to omit the attribute completely.  |
| `validate_inners_is_tuple`            | Function | Guarantees that the structural components container is formatted as a native tuple.  |
"""