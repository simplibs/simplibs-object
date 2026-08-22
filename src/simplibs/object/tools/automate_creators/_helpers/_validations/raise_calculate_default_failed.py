from typing import Any, Callable, NoReturn
# Outers
from .....exceptions import SimpleRuntimeError


def raise_calculate_default_failed(
    logic: Callable,
    params: tuple[Any, ...],
    original_exception: Exception,
) -> NoReturn:

    """Raises a structured error when logic invocation fails during default value calculation."""

    logic_name = getattr(logic, "__name__", str(logic))

    raise SimpleRuntimeError(
        error_name="CALCULATE DEFAULT FAILED ERROR",
        label="calculate_default_failed",
        expected="A valid logic callable that executes successfully with default inner values",
        value={
            "logic": logic_name,
            "params": params,
        },
        problem=(
            f"Failed to infer default value using logic function '{logic_name}'. ",
            f"Execution raised {type(original_exception).__name__}: {original_exception}"
        ),
        context=(
            f"Attempted to execute logic '{logic_name}' with inferred inner default arguments, ",
            f"to automatically determine the value type of a dynamic composite object."
        ),
        how_to_fix=(
            "Ensure the provided 'logic' callable handles initial default child values without raising exceptions.",
            "Verify that default values of all 'inners' are compatible with the operations inside 'logic'.",
            "Alternatively, explicitly specify the 'value_type' parameter in create_object_class / create_simple_object.",
        ),
        exception=original_exception,
    )


_DESIGN_NOTES = """
# raise_calculate_default_failed

## Purpose
Provides diagnostic feedback when automatic type inference fails due to an error during `logic` execution.

## Behavior
1. Captures the original exception raised by `logic`.
2. Wraps it into a structured `SimpleRuntimeError`.
3. Advises either fixing default values in child nodes or providing explicit `value_type`.
"""