from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inners_is_not_empty(
    inners: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_inners' collection is not an empty tuple."""

    # 1. Exception condition
    if isinstance(inners, tuple) and not inners:

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="The '_inners' attribute is an empty tuple",
            expected="A non-empty tuple containing subclasses of SimpleConstant or SimpleObject.",
            value=inners,
            problem=f"The '_inners' attribute on class '{class_name}' points to an empty tuple container.",
            context=context,
            how_to_fix=(
                "Ensure that the '_inners' attribute is correctly declared with at least one element.",
                "The '_inners' collection cannot be empty; if this class has no inner components, remove the '_inners' attribute completely so it behaves as a constant.",
            ) + acceptable_definitions,
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_inners_is_not_empty

## Purpose
Ensures structural clarity and enforces the architectural boundary between constants 
and compositions. An empty `_inners` tuple represents an invalid semantic state within 
the framework.

## Why Emptiness is Forbidden
1. **Architectural Dichotomy**: The presence of `_inners` classifies a class as a 
   composition (`SimpleObject`). If there are no inner items, the class should not 
   declare `_inners` at all, allowing it to naturally fall back to a constant state (`SimpleConstant`).
2. **Signature Integrity**: Downstream template processors map inner items to dynamic 
   positional arguments inside generated methods. An empty collection would result in a 
   redundant, empty signature layout, polluting the reflection API layer.

## Error Strategy
Triggers a `ValueError` wrapper rather than a generic type check. This signals to the 
developer that while the container wrapper type itself is valid (`tuple`), its current content 
state makes it impossible to continue class compilation.
"""