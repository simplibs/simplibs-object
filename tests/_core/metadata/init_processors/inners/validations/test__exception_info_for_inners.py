from typing import TYPE_CHECKING, Tuple
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def _exception_info_for_inners(
    owner_class: "SimpleClassLike",
) -> Tuple[str, str, str, Tuple[str, ...]]:
    """Provides shared diagnostic info for inners validation."""

    class_name = owner_class.__name__
    error_name = "INVALID INNERS DEFINITION"
    context = f"{class_name}._inners validation"

    acceptable = (
        "Acceptable definition:",
        f"class {class_name}(SimpleObject):",
        "    _inners = (FirstElement, SecondElement)",
    )

    return class_name, error_name, context, acceptable



_DESIGN_NOTES = """
# _exception_info_for_inners

## Purpose
Provides shared diagnostic information for all inners‑validation functions:
- class name,
- error label,
- context string,
- example of acceptable definition.

## Behavior
Returns a 4‑tuple used by all validation functions to build consistent error
messages.

## Notes
This helper is internal to the inners‑validation pipeline and is not part of the
public API.
"""