from typing import Any, NoReturn
from simplibs.sentinels import UNSET
# Outers
from ....exceptions import SimpleLogicError


def validate_constant_has_not_logic(class_name: str, logic: Any) -> None | NoReturn:
    """Validates that a constant leaf class definition does not provide a logic calculation rule."""

    if logic is not UNSET:
        raise SimpleLogicError(
            error_name="CONSTANT LOGIC CONFLICT ERROR",
            label="constant_logic_conflict",
            expected="logic=UNSET when creating a SimpleConstant class",
            value=logic,
            problem=f"Constant class '{class_name}' received a 'logic' parameter, which is reserved for composite objects.",
            context=f"Dynamic creator detected 'inners' was UNSET but received 'logic' for class '{class_name}'.",
            how_to_fix=(
                "SimpleConstant leaf nodes store raw static values and do not support calculation rules ('logic').",
                "If this is a leaf node: remove the 'logic' argument. Allowed constant parameters: 'default', 'value_type', 'validate'.",
                "If this is a composite node: provide the 'inners' tuple specifying child component types alongside 'logic'.",
                "Required for composites: 'inners', 'logic'. Optional for composites: 'decompose', 'validate', 'value_type'.",
            ),
            exception=ValueError,
        )


_DESIGN_NOTES = """
# validate_constant_has_not_logic

## Purpose
Prevents assigning a calculation rule (`logic`) to atomic `SimpleConstant` leaf nodes.

## Behavior
1. Ensures `logic` is `UNSET` when `inners` is not supplied.
2. Directs the user to either remove `logic` or supply `inners` to switch to composite mode.
"""