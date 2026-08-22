from typing import TYPE_CHECKING, Any
# Inners
from .validations import raise_class_not_decomposeable
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleObjectProtocol


def decompose_value(
    cls: "SimpleObjectProtocol",
    value: Any,
) -> Any:
    """Decomposes a composite value into its inner components."""

    # 1. Ensure the composite supports decomposition
    if not cls.meta.is_decomposeable:
        raise_class_not_decomposeable(cls.meta)

    # 2. Validate the provided value
    cls.validate(value)

    # 3. Perform decomposition using the class's decompose function
    outcome = cls.meta.decompose(value)

    # 4. Return the decomposed result
    return outcome



_DESIGN_NOTES = """
# decompose_value

## Purpose
Provides the public-facing entry point for decomposing a composite value into its
inner components. This function ensures that decomposition is supported by the
class and that the provided value is valid before invoking the user-defined
`_decompose` method.

---

## Pipeline Overview

### 1. Decomposability Check
Before any decomposition occurs, the system verifies that the composite class
supports decomposition. If the class is not marked as `is_decomposeable`, a
structured error is raised via `raise_class_not_decomposeable`.

### 2. Validation
The provided value is validated using the full validation pipeline:

- type validation,
- user-defined validation,
- normalization rules (if applicable).

This ensures that decomposition is performed only on valid, well-formed values.

### 3. Decomposition
After validation, the function calls:

```
cls.meta.decompose(cls, value)
```

This delegates the actual decomposition logic to the user-defined `_decompose`
method, if provided. If `_decompose` is not implemented, metadata ensures that
the class is marked as non-decomposable.

### 4. Result Delivery
The return value of `_decompose` becomes the decomposed representation of the
composite value.

---

## Why this function exists
Composite objects may optionally support decomposition. This function provides:

- a stable API for users,
- consistent validation before decomposition,
- predictable behavior across all composite classes,
- separation of concerns (validation vs. decomposition),
- safety guarantees through decomposability checks.

---

## Notes
- This function is attached to `SimpleObject` as a class method.
- The public-facing documentation belongs to `SimpleObject.decompose_value`.
- All diagnostics are delegated to the validation pipeline and
  `raise_class_not_decomposeable`.
```
"""
