from typing import TYPE_CHECKING
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike


def raise_class_not_decomposeable(
    meta: "SimpleMetadataLike",
) -> None:
    """Raises an error when a composite value cannot be assigned directly."""

    class_name = meta.class_name

    # 1. Determine whether the class itself lacks a decompose method
    has_decompose = meta.decompose is not None and meta.decompose is not UNSET

    # 2. Identify inner composite nodes that break decomposability
    offenders = [
        inner for inner in meta.inners
        if not inner.meta.is_constant and not inner.meta.is_decomposeable
    ]
    offender_names = ", ".join(o.meta.class_name for o in offenders) or "None"

    # 3. Build human-facing explanation
    if not has_decompose:
        reason = (
            f"Composite '{class_name}' does not define a method for decomposing values."
        )
    else:
        reason = (
            f"Composite '{class_name}' defines a decomposition method, "
            f"but some of its inner composite elements cannot be decomposed."
        )

    raise SimpleLogicError(
        error_name="COMPOSITE VALUE ASSIGNMENT ERROR",
        label="composite_not_decomposeable",
        expected="A composite that supports direct value assignment",
        value=class_name,
        problem=f"Direct assignment of a value to composite '{class_name}' is not possible. ",
        context=(
            f"{reason}",
            f"Inner non-decomposable elements: {offender_names}."
        ),
        how_to_fix=(
            "This composite cannot accept a value directly because it cannot decompose "
            "the provided value into its inner elements.",
            "You can still modify the composite by changing its constant inner values, "
            "which will update the composite from the bottom up.",
            "If the composite is intentionally non-decomposable, this behavior is expected."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_class_not_decomposeable

## Purpose
This exception is user-facing. It informs the user that a composite value cannot
be assigned directly because the composite structure cannot decompose the
incoming value into its inner elements.

## Behavior
- If the composite class itself lacks a `decompose_value` method, the error
  explains that direct assignment is impossible.
- If the composite class *does* define a decomposition method but one or more
  inner composite nodes are non-decomposable, the error identifies those nodes.
- Constant inners are ignored, because they do not require decomposition.

## Notes
- This is not a developer guidance error. It does not instruct the programmer to
  implement `decompose_value`. Instead, it explains to the *user* why the value
  cannot be set directly.
- The error clarifies that the composite can still be modified indirectly by
  changing constant inner values, which propagate upward.
- A composite may intentionally be non-decomposable; this exception respects
  that design and communicates it clearly.
"""