from typing import Any, Callable
# Inners
from ._is_lambda import _is_lambda


def process_validate(
    validate: Callable
) -> Callable:
    """Normalizes a validation callable to ensure a unified (cls, value, *, return_bool) signature.

    If the provided ``validate`` handler is an anonymous lambda, wraps it into a classmethod-compatible
    closure that accepts the class context (``cls``) and optional keyword arguments while executing
    the single-argument lambda.

    Args:
        validate: Raw validation function or lambda callable.

    Returns:
        A normalized callable adhering to the standard (cls, value, *, return_bool=False) signature.
    """

    # 1. Return regular named functions directly
    if not _is_lambda(validate):
        return validate

    # 2. Wrap anonymous lambda to accept (cls, value, *, return_bool=False) signature
    def _validate(cls: Any, value: Any, *, return_bool: bool = False):
        return validate(value)

    return _validate


_DESIGN_NOTES = """
# process_validate (Internal Helper Engine)

## Purpose
Normalizes user-supplied validation rules for both `SimpleConstant` and `SimpleObject` blueprints.
Anonymous lambdas typically accept only a single value argument (e.g. `lambda val: val > 0`);
this helper wraps them so they can be mounted as `classmethod` handlers accepting `(cls, value, *, return_bool=False)`.

## Execution Workflow
1. Checks if `validate` is an anonymous lambda using `_is_lambda`.
2. If it is a regular named function, returns it untouched.
3. If it is a lambda, returns a closure `_validate(cls, value, *, return_bool=False)` that forwards `value` to the lambda.

## Framework Usage
- Internal helper invoked exclusively within `create_constant_class` and `create_object_class`.
"""