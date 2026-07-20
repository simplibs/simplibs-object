from typing import TYPE_CHECKING
# Inners
from .exception_context_for_classmethod import exception_context_for_classmethod
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol
    from .ClassMethodExceptionInfoPayload import ClassMethodExceptionInfoPayload


def exception_info_for_classmethod(
    bound_method: "ClassMethodProtocol",
    expected_params: tuple[str, ...],
    expected_args_params_count: int
) -> "ClassMethodExceptionInfoPayload":
    """Generates comprehensive diagnostic descriptors and structural blueprints for method validation errors."""

    # 1. Harvest base identity parameters via structural extraction dictionary
    base_info = exception_context_for_classmethod(bound_method)
    class_name = base_info["class_name"]
    context = base_info["context"]

    # Resolve the proper parent class template for explicit visualization instructions
    class_parent = "SimpleObject" if "SimpleObject" in [c.__name__ for c in bound_method.__self__.__mro__] else "SimpleConstant"

    # 2. Segment positional parameters and keyword-only configurations
    args_params = ", ".join(expected_params[:expected_args_params_count])
    kwargs_params = ", ".join(expected_params[expected_args_params_count:])

    # 3. Assemble target signature presentation
    params_signature = f"{args_params}" + (f", *, {kwargs_params}" if kwargs_params else "")

    # 4. Construct copy-paste ready blueprint for user remediation
    expected_structure: tuple[str, ...] = (
        "Expected structure:",
        f"class {class_name}({class_parent}):",
        "    ...",
        "    @classmethod",
        f"    def {base_info['method_name']}({params_signature}):",
        "        ..."
    )

    # 5. Yield complete diagnostic payload dictionary
    return {
        "class_name": class_name,
        "method_name": base_info["method_name"],
        "expected_structure": expected_structure,
        "context": context
    }


_DESIGN_NOTES = """
# exception_info_for_classmethod

## Purpose
This helper functions as a code blueprint generator for developer remediation. When signature validation 
fails (e.g., incorrect argument count, missing keywords, misconfigured types), this utility creates 
a copy-paste ready structural mock up of exactly how the class method should be declared in the source file.

## Design Decisions
1. **MRO Inspection**: It dynamically inspects the Method Resolution Order (`__mro__`) to identify 
   if the target is a `SimpleObject` or a `SimpleConstant`, making the generated code example highly specific.
2. **Keyword-Only Separation**: It respects Python signature protocols, injecting the `*,` separator 
   if the validation expects keyword-only arguments (`kwargs_params`).
3. **Dictionary Integration**: Integrates directly with `exception_context_for_classmethod` by unpacking 
   its dictionary values and returning an expanded dictionary payload containing the full remediation blueprint.
"""