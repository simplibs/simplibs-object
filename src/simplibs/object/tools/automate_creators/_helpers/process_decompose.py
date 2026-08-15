from typing import Any, Callable
# Inners
from ._is_lambda import _is_lambda


def process_decompose(
    decompose: Callable
) -> Callable:
    """Normalizes a decompose callable to ensure a unified (cls, value) signature.

    If the provided ``decompose`` handler is an anonymous lambda, wraps it to accept
    and ignore the class instance context (``cls``) argument automatically.

    Args:
        decompose: Raw decompose function or lambda handler.

    Returns:
        A normalized callable adhering to the standard (cls, value) method signature.
    """

    # 1. Return regular functions directly
    if not _is_lambda(decompose):
        return decompose

    # 2. Wrap anonymous lambda to accept (cls, value) signature
    def _decompose(cls: Any, value: Any) -> Any:
        return decompose(value)

    return _decompose


_DESIGN_NOTES = """
# process_decompose (Internal Helper Engine)

## Purpose
Normalizes user-supplied `decompose` callables for composite object blueprints. Anonymous lambda 
functions typically accept only a single value argument `lambda val: ...`; this helper wraps them 
so that the framework can invoke `_decompose(cls, value)` uniformly.

## Execution Workflow
1. Checks if `decompose` is an anonymous lambda using `_is_lambda`.
2. If it is a regular named function, returns it untouched.
3. If it is a lambda, wraps it into a closure `_decompose(cls, value)` that passes only `value` to the lambda.

## Framework Usage
- Internal helper invoked exclusively within `create_object_class`.
"""