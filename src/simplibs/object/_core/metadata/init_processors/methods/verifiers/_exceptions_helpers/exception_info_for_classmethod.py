from typing import Any


def exception_info_for_classmethod(
    bound_method: Any,
) -> tuple[str, str, str]:
    """Extracts class name, method name, and diagnostic context safely."""

    # 1. Class name recovery (fallback to <UnknownClass>)
    owner = getattr(bound_method, "__self__", None)
    class_name = owner.__name__ if owner is not None else "<UnknownClass>"

    # 2. Method name recovery (fallback to standard string/attribute inspection)
    func = getattr(bound_method, "__func__", bound_method)
    method_name = getattr(func, "__name__", str(bound_method))

    # 3. Build diagnostic context
    context = f"Metadata validation for: {class_name}.{method_name}"

    return (
        class_name,
        method_name,
        context,
    )


_DESIGN_NOTES = """
# exception_info_for_classmethod

## Purpose
Provides minimal diagnostic metadata (class name, method name, diagnostic context)
for classmethod validation exceptions.

## Defensive Behavior
The function handles invalid user-provided inputs safely:
- Extracts class name via `__self__`, falling back to `<UnknownClass>` if `bound_method`
  is not a bound classmethod (e.g., plain string, lambda, or un-bound function).
- Extracts method name via `__func__.__name__`, falling back to `str(bound_method)`.

## Why tuple
The returned values are:
- fixed in structure,
- used immediately,
- immutable,
- not stored or exposed externally.

A tuple is the fastest and cleanest option.

## Separation of concerns
This helper is intentionally small and focused only on identity metadata.
The full structural code blueprint is delegated to `expected_structure_for_classmethod`.
"""