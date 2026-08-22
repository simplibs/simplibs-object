from simplibs.exception import SimpleException


class SimpleObjectError(SimpleException):
    """
    Base exception class for all errors originating from the SimpleObject library.

    This class is not intended to be raised directly. Instead, it serves as the
    common ancestor for all specific Simple-related exceptions, allowing users
    to catch any library-level error using a single `except SimpleObjectError` block.
    """

    # Skip internal library frames when generating error location metadata.
    # This ensures that error messages point to user code rather than internal
    # implementation details, unless no user-level frames remain.
    _skip_locations = ("simplibs/object",)


_DESIGN_NOTES = """
# SimpleObjectError — Root Exception for the Simple Library

## Purpose
`SimpleObjectError` is the umbrella exception for the entire SimpleObject ecosystem.
It provides a unified base class for all errors thrown by the library, allowing
users to catch any Simple-related issue using a single exception type.

This class is not meant to be raised directly. Instead, it acts as the root of
the exception hierarchy, ensuring consistent behavior, predictable grouping, and
clean error reporting.

---

## 1. Error Location Filtering (`_skip_locations`)
The attribute:

```python
_skip_locations = ("simplibs/object",)

```

instructs the underlying `SimpleException` engine to skip internal frames
originating from the SimpleObject library when generating error location
metadata.

This ensures that:

* error messages point to **user code**, not internal implementation,
* internal frames are shown **only when necessary** (e.g., when no user frames
remain),
* developers receive clean, readable diagnostics.

This behavior is essential for library authors and is automatically inherited by
all Simple-related exceptions.

---

## 2. Subclasses

### `SimpleDefinitionError`

Definition-time exception raised when processing metadata or class blueprints.
Signals structural errors made during code writing (e.g., malformed `_inners`,
forbidden `_default` on composites). Main consumer: Metadata logic.

### `SimpleInitializationError`

Instantiation-time exception raised during `__init__` or `__new__` pipeline.
Signals incompatible runtime creation parameters, missing requirements, or
mixin composition conflicts. Main consumer: Instance and mixin initialization logic.

### `SimpleRuntimeError`

Data-level exception raised during execution when values fail validation,
normalization, or state rules. This is the primary public exception that end
users encounter during normal application usage.

### `SimpleRuntimeError`

Utility exception raised exclusively by test-assistance functions (e.g., fuzz-filling
or randomized data generation). Signals exhausted retries or unsupported test setups.

---

## 3. Catch-All Grouping

Users can catch all Simple-related errors using:

```python
try:
    # SimpleObject operations
    ...
except SimpleObjectError:
    # Handle any error thrown by the SimpleObject library
    ...

```

This provides a clean and predictable error-handling strategy.

---

## Notes

* All Simple exceptions inherit from `SimpleObjectError`.
* This class ensures consistent behavior across the entire library.
* Error location filtering is inherited automatically by all subclasses.
"""