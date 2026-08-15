from typing import Any, NoReturn
from simplibs.sentinels import UNSET
# Outers
from ....exceptions import SimpleLogicError


def validate_composite_has_logic(class_name: str, logic: Any) -> None | NoReturn:
    """Validates that a composite object class definition provides a valid logic calculation callable."""

    if logic in (UNSET, None):
        raise SimpleLogicError(
            error_name="COMPOSITE MISSING LOGIC ERROR",
            label="composite_missing_or_none_logic",
            expected="A valid non-None and non-UNSET callable logic function (logic not in (UNSET, None))",
            value=logic,
            problem=(
                f"Composite class '{class_name}' specifies 'inners' but is missing the required 'logic' "
                f"calculation rule (received: {logic!r})."
            ),
            context=(
                f"Dynamic creator inferred composite mode for class '{class_name}' because 'inners' was provided, "
                f"but a valid logic pipeline was not supplied."
            ),
            how_to_fix=(
                "SimpleObject composites must derive their value from inner child components via a 'logic' function.",
                "Provide a callable 'logic' function (or lambda) accepting parameters corresponding to inner snake_case names.",
                "Do not pass None or UNSET for 'logic' when defining composite objects.",
                "Required for composites: 'inners', 'logic'. Optional: 'decompose', 'validate', 'value_type'.",
                "If this is a leaf constant: remove 'inners' and provide a static 'default' value instead.",
            ),
            exception=ValueError,
        )


_DESIGN_NOTES = """
# validate_composite_has_logic

## Purpose
Guarantees that every composite `SimpleObject` defines a functional `logic` pipeline for value derivation.

## Behavior
1. Asserts `logic` is not in `(UNSET, None)` when `inners` is present.
2. Raises structured `SimpleLogicError` emphasizing mandatory calculation rules for composite nodes.
"""