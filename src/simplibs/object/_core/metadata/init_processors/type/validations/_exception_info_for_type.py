# Annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def _exception_info_for_type(
    owner_class: "SimpleClassLike",
) -> tuple[str, str, str, str, tuple[str, ...]]:
    """Collects diagnostic data for type‑related validation errors."""

    # 1. Basic identifiers
    attribute_name = "_type"
    class_name = owner_class.__name__

    # 2. Parent type (constant vs object)
    from ......SimpleObject import SimpleObject
    class_parent = (
        "SimpleObject"
        if SimpleObject in owner_class.__mro__
        else "SimpleConstant"
    )

    # 3. Error metadata
    error_name = "INVALID TYPE DEFINITION"
    context = f"Metadata validation for: {class_name}.{attribute_name}"

    # 4. Acceptable definitions
    acceptable_definitions = (
        "Acceptable definitions:",
        f"class {class_name}({class_parent}):",
        f"    {attribute_name} = int",
        f"    {attribute_name} = int | str",
        f"    {attribute_name} = (int, str)",
        "    ...",
    )

    return (
        class_name,
        class_parent,
        error_name,
        context,
        acceptable_definitions,
    )



_DESIGN_NOTES = """
# _exception_info_for_type

## Purpose
Provides a centralized source of diagnostic strings for all type‑related
validation errors. This keeps validation functions clean and avoids repeating
the same formatting logic.

## How it works
The helper extracts:

- the class name,
- whether the class is a `SimpleConstant` or `SimpleObject`,
- the error name,
- a contextual description,
- a list of acceptable `_type` definitions.

These values are returned as a fixed tuple and immediately unpacked by the
validation functions.

## Why tuple is used
The returned data is:

- fixed in structure,
- used only once,
- not mutated,
- not stored,
- not exposed to the user.

Tuple is the fastest and cleanest option for this one‑shot usage pattern.

## Parent detection
The helper inspects the class MRO to determine whether the class belongs to the
constant or object branch. This allows error messages to show accurate example
definitions.

## Notes
The examples use assignment (`=`) rather than type hints (`:`), matching how
SimpleObject metadata is defined inside class bodies.

"""