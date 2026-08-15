from typing import NoReturn
# Outers
from ....exceptions import SimpleLogicError


def raise_inner_value_empty_path() -> NoReturn:
    """Raises a structured error when an InnerValue path resolution yields an empty path."""

    raise SimpleLogicError(
        error_name="INNER VALUE EMPTY PATH ERROR",
        label="path",
        expected="A non-empty string path (e.g. 'address.city') or iterable of path parts.",
        problem=(
            "Provided path evaluated to an empty sequence.",
            "An InnerValue requires a valid target property path to perform navigation."
        ),
        context="Attempted to construct an InnerValue container with an empty string or empty sequence.",
        how_to_fix=(
            "Ensure the path parameter is a dot-separated string like 'age' or 'address.city'.",
            "Do not pass empty strings '' or empty tuples/lists () as the path."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_inner_value_empty_path

## Purpose
Raises a structured `SimpleLogicError` when an `InnerValue` instance is constructed 
with an empty path specification.

## Why this validation exists
`InnerValue` is designed to target and mutate nested properties on composite test objects. 
An empty path cannot be navigated or resolved to a target property.

## Execution context
Called in `InnerValue.__post_init__` if the normalized path sequence contains no elements.
"""