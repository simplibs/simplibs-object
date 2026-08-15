from typing import Any, Callable, Iterable
# Inners
from ._is_lambda import _is_lambda


def process_logic(
    logic: Callable,
    params_name: Iterable[str]
) -> Callable:
    """Normalizes a logic calculation callable to ensure a unified (cls, *args) signature.

    If the provided ``logic`` callable is an anonymous lambda, dynamically compiles
    a wrapper function via ``exec`` that accepts the class context (``cls``) alongside
    all named child inner parameters.

    Args:
        logic: Raw logic function or lambda calculation rule.
        params_name: Iterable of parameter snake_case names derived from inner components.

    Returns:
        A normalized callable adhering to the standard (cls, *params) method signature.
    """

    # 1. Return regular named functions directly
    if not _is_lambda(logic):
        return logic

    # 2. Build parameter signature string from inner names
    params = ", ".join(params_name)
    src = f"def _logic(cls, {params}): return logic({params})"

    # 3. Dynamically compile wrapper function
    namespace: dict[str, Any] = {"logic": logic}
    exec(src, namespace)

    # 4. Return compiled logic wrapper
    return namespace["_logic"]


_DESIGN_NOTES = """
# process_logic (Internal Helper Engine)

## Purpose
Normalizes user-supplied calculation logic for composite object blueprints. Lambda functions 
typically omit the implicit `cls` context argument (e.g. `lambda a, b: a + b`); this helper 
dynamically wraps the lambda using `exec` to create a standard `_logic(cls, a, b)` signature.

## Execution Workflow
1. Checks if `logic` is an anonymous lambda using `_is_lambda`.
2. If it is a regular function, returns it untouched.
3. Joins `params_name` into a comma-separated parameter string.
4. Dynamically compiles a signature-correct wrapper via `exec` in a local namespace.
5. Extracts and returns the compiled `_logic` function.

## Framework Usage
- Internal helper invoked exclusively within `create_object_class`.
"""