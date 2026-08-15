from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.methods import ClassMethodProtocol


def exception_info_for_classmethod(
    bound_method: "ClassMethodProtocol",
) -> tuple[str, str, str]:
    """Extracts class name, method name, and diagnostic context."""

    class_name = bound_method.__self__.__name__
    method_name = bound_method.__func__.__name__
    context = f"Metadata validation for: {class_name}.{method_name}"

    return (
        class_name,
        method_name,
        context,
    )


_DESIGN_NOTES = """
# exception_info_for_classmethod

## Purpose
Provides the minimal diagnostic metadata needed for most classmethod validations:
- class name
- method name
- context string

## Why tuple
The returned values are:
- fixed in structure,
- used immediately,
- not mutated,
- not stored,
- not exposed externally.

Tuple is the fastest and cleanest option.

## Separation of concerns
This helper is intentionally small.  
It is used when validation needs only basic identity information.

The larger helper (expected structure) will be a separate function returning only
the code‑blueprint tuple, not an extended version of this one.
"""