from simplibs.exception import SimpleException


class SimpleError(SimpleException):
    """Base exception for the entire SimpleObject library."""

    _skip_locations = ("simplibs/object",)


_DESIGN_NOTES = """
# SimpleError

## Purpose
The main umbrella exception for the entire `SimpleObject` ecosystem. It is not intended to be raised directly, but serves as a common ancestor for all errors within the library.

## Subclasses
The following specific exceptions inherit from this base class:
- `SimpleLogicError`
- `SimpleMetadataError`
- `SimpleMixinError`

## Catch All Grouping
It allows the user to catch any problem associated with this library using a single try-except block:
```python
try:
    # SimpleObject operations
    ...
except SimpleError:
    # Handle any error thrown by the SimpleObject library
    ...

```

"""