from typing import get_args, Union, get_origin, Any
from types import UnionType


def _convert_annotation_to_type_set(
    annotation: type | None | UnionType,
) -> set[type]:
    """Converts annotation or union into a flat set of types."""

    # 1. Single type
    if isinstance(annotation, type):
        return {annotation}

    # 2. Union or PEP 604 pipe union
    if isinstance(annotation, UnionType) or get_origin(annotation) is Union:
        return set(get_args(annotation))

    # 3. Fallback
    return {Any}



_DESIGN_NOTES = """
# _convert_annotation_to_type_set

## Purpose
Normalizes Python type annotations into a flat `set[type]` so that
`validate_annotations` can perform simple subset checks.

## Behavior
1. Single types → `{type}`
2. `Union` or PEP 604 unions → `{t1, t2, ...}`
3. Anything else → `{Any}` as a safe fallback

## Why separate
This function is a pure utility.  
Keeping it isolated makes `validate_annotations` smaller, cleaner, and easier to test.
"""