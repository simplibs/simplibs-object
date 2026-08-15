from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.methods import ClassMethodProtocol


def expected_structure_for_classmethod(
    bound_method: "ClassMethodProtocol",
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> tuple[str, ...]:
    """Generates a copy‑paste ready expected method structure."""

    class_name = bound_method.__self__.__name__
    method_name = bound_method.__func__.__name__

    class_parent = (
        "SimpleObject"
        if "SimpleObject" in [c.__name__ for c in bound_method.__self__.__mro__]
        else "SimpleConstant"
    )

    args_params = ", ".join(expected_params[:expected_args_params_count])
    kwargs_params = ", ".join(expected_params[expected_args_params_count:])

    params_signature = (
        f"{args_params}"
        + (f", *, {kwargs_params}" if kwargs_params else "")
    )

    expected_structure = (
        "Expected structure:",
        f"class {class_name}({class_parent}):",
        "    ...",
        "    @classmethod",
        f"    def {method_name}({params_signature}):",
        "        ...",
    )

    return expected_structure



_DESIGN_NOTES = """
# expected_structure_for_classmethod

## Purpose
Generates a minimal, copy‑paste ready code blueprint showing how the classmethod
should be declared.  
Used when signature validation fails and the developer needs a clear structural
example of the correct method layout.

## What it returns
Only one value:

- `expected_structure` — a tuple of strings forming a readable code snippet.

The function does not return class name, method name, or context separately.
It computes these values internally and embeds them directly into the blueprint.

## Why this separation exists
The method‑validation pipeline uses two helpers:

- **exception_context_for_classmethod**  
  Provides minimal identity metadata (class name, method name, context).

- **exception_info_for_classmethod**  
  Provides the full structural code example.

Each helper has a distinct purpose and remains independent.

## Why tuple
The expected structure:

- has a fixed shape,
- is immutable,
- is consumed immediately,
- does not require keys or dictionary access.

A tuple is the cleanest and fastest representation.

## Notes
This helper is used only when the developer needs to see the correct method
signature visually.  
It is intentionally simple and focused solely on generating the blueprint.
"""