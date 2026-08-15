from typing import Any, NoReturn
from simplibs.sentinels import UNSET
# Outers
from ....exceptions import SimpleLogicError


def validate_composite_has_not_default(class_name: str, default: Any) -> None | NoReturn:
    """Validates that a composite object class definition does not provide a static default value."""

    if default is not UNSET:
        raise SimpleLogicError(
            error_name="COMPOSITE DEFAULT CONFLICT ERROR",
            label="composite_default_conflict",
            expected="default=UNSET when creating a SimpleObject composite class",
            value=default,
            problem=f"Composite class '{class_name}' received a 'default' parameter, which is reserved for leaf constants.",
            context=f"Dynamic creator detected 'inners' tuple was provided for composite class '{class_name}'.",
            how_to_fix=(
                "SimpleObject composite values are dynamically derived from child 'inners' via 'logic' calculation.",
                "If this is a composite node: remove the 'default' argument.",
                "Required for composites: 'inners', 'logic'. Optional for composites: 'decompose', 'validate', 'value_type'.",
                "If this is a leaf constant: remove 'inners' and 'logic'. Constants require: 'default' (optional: 'validate', 'value_type').",
            ),
            exception=ValueError,
        )


_DESIGN_NOTES = """
# validate_composite_has_not_default

## Purpose
Prevents setting a static default on composite nodes whose values must be computed via `logic`.

## Behavior
1. Verifies `default` is `UNSET` when `inners` is supplied.
2. Guides the developer to remove `default` or switch to constant mode by removing `inners`.
"""