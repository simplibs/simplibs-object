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

    # 1. Class name recovery (fallback to <UnknownClass>)
    owner = getattr(bound_method, "__self__", None)
    class_name = owner.__name__ if owner is not None else "<UnknownClass>"

    # 2. Method name recovery (fallback to standard string/attribute inspection)
    func = getattr(bound_method, "__func__", bound_method)
    method_name = getattr(func, "__name__", str(bound_method))

    # 3. Safe parent recovery via already resolved owner
    if owner is None:
        class_parent = "<UnknownClass>"
    else:
        mro_names = [c.__name__ for c in getattr(owner, "__mro__", ())]
        class_parent = "SimpleObject" if "SimpleObject" in mro_names else "SimpleConstant"

    # 4. Build signature parameters
    args_params = ", ".join(expected_params[:expected_args_params_count])
    kwargs_params = ", ".join(expected_params[expected_args_params_count:])

    params_signature = (
        f"{args_params}"
        + (f", *, {kwargs_params}" if kwargs_params else "")
    )

    # 5. Build blueprint structure
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
Generates a copy-paste ready code blueprint showing how a required `@classmethod`
should be declared. Used when signature validation fails.

## Defensive Behavior & Parent Discovery
- Safely extracts class name via `bound_method.__self__`, falling back to `<UnknownClass>`.
- Dynamically discovers the parent class (`SimpleObject` vs `SimpleConstant`) by inspecting
  the `owner.__mro__`.
- Formats positional and keyword-only arguments separated by `*, ` according to strict protocol specs.

## What it returns
- `expected_structure` — a tuple of strings forming a readable multi-line code snippet.

## Why this separation exists
The method-validation pipeline uses two distinct helpers:
- **exception_info_for_classmethod**: Provides identity metadata (class name, method name, context).
- **expected_structure_for_classmethod**: Generates the structural blueprint code snippet.

Each helper maintains a single responsibility and operates independently.

## Why tuple
The expected structure:
- has a fixed layout,
- is immutable,
- is consumed immediately for error formatting.
"""