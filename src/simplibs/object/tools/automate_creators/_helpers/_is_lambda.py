from typing import Any


def _is_lambda(fn: Any) -> bool:
    """Determines whether a given object is a lambda function.

    Args:
        fn: Candidate object to inspect.

    Returns:
        True if fn is a callable lambda function, False otherwise.
    """

    return (
        callable(fn)
        and getattr(fn, "__name__", None) == "<lambda>"
    )


_DESIGN_NOTES = """
# _is_lambda (Helper Predicate)

## Purpose
Provides a lightweight inspection check to determine if a provided function or validation rule 
is an anonymous lambda callable (`<lambda>`).

## Execution Workflow
1. Checks whether the argument is callable using `callable(fn)`.
2. Inspects `__name__` safely via `getattr` to verify it equals `"<lambda>"`.

## Framework Usage
- Used by `process_validate` and `process_logic` wrappers to detect anonymous callables 
  and adjust argument reflection behavior accordingly.
"""