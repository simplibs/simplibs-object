from typing import Any, Callable
# Inners
from ._validations import raise_calculate_default_failed


def calculate_default(
    logic: Callable,
    params: tuple[Any, ...]
) -> Any:
    """Calculates the initial default value of a composite object by invoking its logic function.

    Executes the provided ``logic`` callable using default values from child inner nodes.
    This result is typically used to infer the output ``value_type`` when omitted during dynamic creation.

    Args:
        logic: Callable function defining composite logic calculation.
        params: Tuple of default values extracted from inner components.

    Returns:
        The computed default result of the logic function.

    Raises:
        SimpleRuntimeError: If logic execution fails with provided default parameters.
    """

    # 1. Execute Logic Callable with Default Inner Arguments
    try:
        cls = None
        return logic(cls, *params)

    # 2. Capture Logic Failures & Raise Structured Error
    except Exception as exc:
        raise_calculate_default_failed(logic, params, exc)


_DESIGN_NOTES = """
# calculate_default (Helper Engine)

## Purpose
Executes a composite object's `logic` callable at blueprint setup time using default values 
extracted from inner children. The resulting value allows the framework to infer `value_type` 
automatically without requiring explicit type hints from the user.

## Execution Workflow
1. Invokes `logic(None, *params)` passing dummy class context (`cls=None`) and inner defaults.
2. Returns the evaluated default value.
3. On exception, delegates to `raise_calculate_default_failed` to produce structured diagnostics.

## Framework Usage
- Invoked exclusively inside `create_object_class` when `value_type` is `UNSET`.
"""