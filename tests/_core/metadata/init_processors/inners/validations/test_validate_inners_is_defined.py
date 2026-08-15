from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_inners_is_defined(
    attribute_value: Any,
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that '_inners' is explicitly defined."""

    # 1. Check definition
    if attribute_value is not UNSET:
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Raise error
    raise SimpleMetadataError(
        error_name=error_name,
        label="_inners_missing",
        expected="Explicit '_inners' tuple",
        value=attribute_value,
        problem=f"Class '{class_name}' does not define '_inners'.",
        context=context,
        how_to_fix=(
            f"Define '_inners' inside class '{class_name}'.",
            "Example:",
        ) + acceptable,
        exception=AttributeError,
    )



_DESIGN_NOTES = """
# validate_inners_is_defined

## Purpose
Ensures that a composite class explicitly defines the `_inners` attribute.

## Behavior
1. Checks whether `_inners` is UNSET.
2. If missing, retrieves shared diagnostic info from `_exception_info_for_inners`.
3. Raises a structured `SimpleMetadataError`.

## Notes
This validator is used only when `_inners` is expected to exist. It prevents
composite metadata from being processed without structural definitions.
"""