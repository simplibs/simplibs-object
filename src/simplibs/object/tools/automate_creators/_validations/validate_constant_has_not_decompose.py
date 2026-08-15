from typing import Any, NoReturn
from simplibs.sentinels import UNSET
# Outers
from ....exceptions import SimpleLogicError


def validate_constant_has_not_decompose(class_name: str, decompose: Any) -> None | NoReturn:
    """Validates that a constant leaf class definition does not provide a decomposition handler."""

    if decompose is not UNSET:
        raise SimpleLogicError(
            error_name="CONSTANT DECOMPOSE CONFLICT ERROR",
            label="constant_decompose_conflict",
            expected="decompose=UNSET when creating a SimpleConstant class",
            value=decompose,
            problem=f"Constant class '{class_name}' received a 'decompose' parameter, which is reserved for composite objects.",
            context=f"Dynamic creator detected 'inners' was UNSET but received 'decompose' for class '{class_name}'.",
            how_to_fix=(
                "SimpleConstant leaf nodes cannot be decomposed into inner children.",
                "If this is a leaf node: remove the 'decompose' argument. Allowed constant parameters: 'default', 'value_type', 'validate'.",
                "If this is a composite node: provide the 'inners' tuple specifying child component types.",
                "Required for composites: 'inners', 'logic'. Optional for composites: 'decompose', 'validate', 'value_type'.",
            ),
            exception=ValueError,
        )


_DESIGN_NOTES = """
# validate_constant_has_not_decompose

## Purpose
Ensures top-down decomposition callables are not assigned to single leaf constants.

## Behavior
1. Checks if `decompose` is set when `inners` is omitted.
2. Raises structured error clarifying that decomposition is exclusive to composite trees.
"""