from typing import Any, NoReturn
from simplibs.sentinels import UNSET
# Outers
from ....exceptions import SimpleRuntimeError


def validate_composite_has_inners(class_name: str, inners: Any) -> None | NoReturn:
    """Validates that a composite object class definition provides a valid tuple of inner components."""

    if inners in (UNSET, None):
        raise SimpleRuntimeError(
            error_name="COMPOSITE MISSING INNERS ERROR",
            label="composite_missing_or_none_inners",
            expected="A valid non-empty tuple of inner component classes (inners not in (UNSET, None))",
            value=inners,
            problem=(
                f"Attempted to create composite class '{class_name}' without specifying required 'inners' "
                f"child components (received: {inners!r})."
            ),
            context=(
                f"Dynamic creator requires child component blueprints ('inners') to build "
                f"a composite SimpleObject node tree."
            ),
            how_to_fix=(
                "Provide a tuple of child component blueprint classes for 'inners', e.g. inners=(ChildClassA, ChildClassB).",
                "Do not pass None or UNSET for 'inners' when defining composite objects.",
                "Required for composites: 'inners', 'logic'. Optional: 'decompose', 'validate', 'value_type'.",
                "If this is a leaf constant: remove 'logic' and provide a static 'default' value instead.",
            ),
            exception=ValueError,
        )


_DESIGN_NOTES = """
# validate_composite_has_inners

## Purpose
Ensures that composite `SimpleObject` definitions explicitly specify their inner child component classes.

## Behavior
1. Checks if `inners` is in `(UNSET, None)`.
2. Raises structured `SimpleRuntimeError` guiding the developer to pass a valid tuple of child classes.
"""