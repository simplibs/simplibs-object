from typing import Any, NoReturn
# Outers
from ....exceptions import SimpleRuntimeError


def raise_inner_value_invalid_path_type(path: Any, invalid_part: Any) -> NoReturn:
    """Raises a structured error when an InnerValue path contains non-string segment items."""

    raise SimpleRuntimeError(
        error_name="INNER VALUE INVALID PATH TYPE ERROR",
        label="path",
        expected="A string or sequence of string attribute identifiers.",
        value=type(invalid_part).__name__,
        problem=(
            "One or more segments in the provided path are not string identifiers.",
            f"Encountered invalid path segment: {invalid_part!r} of type '{type(invalid_part).__name__}'."
        ),
        context=(
            f"Full path argument provided: {path!r}",
            f"Invalid segment item: {invalid_part!r}",
        ),
        how_to_fix=(
            "Ensure all path segments are valid string property names.",
            "If using a tuple/list path, pass tuples of strings like ('address', 'city', 'zip').",
            "Do not pass integers, objects, or non-string types within the path sequence."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_inner_value_invalid_path_type

## Purpose
Raises a structured `SimpleRuntimeError` when an `InnerValue` instance receives path sequence 
elements that are not string attribute identifiers.

## Why this validation exists
Attribute lookup (`hasattr`/`getattr`) on Python instances strictly requires string property names. 
Encountering non-string elements early prevents runtime type errors during dynamic navigation.

## Execution context
Called in `InnerValue.__post_init__` if any element in the normalized path tuple is not an instance of `str`.
"""