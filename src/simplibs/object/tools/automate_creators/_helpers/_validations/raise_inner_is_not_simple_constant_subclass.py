from typing import Any, NoReturn
# Outers
from .....exceptions import SimpleRuntimeError


def raise_inner_is_not_simple_constant_subclass(
    class_name: str,
    inner: Any
) -> NoReturn:

    inner_repr = getattr(inner, "__name__", repr(inner))

    raise SimpleRuntimeError(
        error_name="INVALID INNER COMPONENT CLASS ERROR",
        label="inner_is_not_simple_constant",
        expected="A class deriving from SimpleConstant / SimpleObject base",
        value=inner_repr,
        problem=(
            f"Item '{inner_repr}' inside 'inners' tuple for class '{class_name}' "
            f"is not a valid Simple framework class subclass."
        ),
        context=(
            f"Inspecting child element blueprints to construct parameter dictionary "
            f"for composite class '{class_name}'."
        ),
        how_to_fix=(
            "Ensure every item inside the 'inners' tuple inherits from SimpleConstant or SimpleObject.",
            "Do not pass primitive types (like int, str) or instantiated objects in the 'inners' tuple.",
            "Pass blueprint classes, e.g. inners=(MyConstantClass, MySubObjectClass).",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_inner_is_simple_constant_subclass

## Purpose
Ensures every child entry within `inners` is a valid class blueprint inheriting from `SimpleConstant`.

## Behavior
1. Checks that `inner` is a `type` and a subclass of `SimpleConstant`.
2. Raises `SimpleRuntimeError` if invalid classes or instances are detected.
"""