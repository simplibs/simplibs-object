from typing import Any, NoReturn
# Outers
from .....exceptions import SimpleLogicError


def raise_inners_is_not_tuple(
    class_name: str,
    inners: Any
) -> NoReturn:

    raise SimpleLogicError(
        error_name="INVALID INNERS CONTAINER TYPE ERROR",
        label="inners_is_not_tuple",
        expected="A tuple containing SimpleConstant subclasses",
        value=type(inners).__name__,
        problem=(
            f"Provided 'inners' argument for composite class '{class_name}' is not a tuple instance. "
            f"Received type '{type(inners).__name__}' instead."
        ),
        context=(
            f"Attempted to inspect child component blueprints for class '{class_name}', "
            f"but container validation failed."
        ),
        how_to_fix=(
            "Wrap inner component classes inside a tuple container, e.g. inners=(FirstInner, SecondInner).",
            "Do not pass lists, sets, or single untupled class references directly.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_inners_is_tuple

## Purpose
Guarantees that the `inners` argument passed to composite creators is structured as an immutable `tuple`.

## Behavior
1. Uses a guard clause checking `isinstance(inners, tuple)`.
2. Raises `SimpleLogicError` wrapping `TypeError` if non-tuple containers are passed.
"""