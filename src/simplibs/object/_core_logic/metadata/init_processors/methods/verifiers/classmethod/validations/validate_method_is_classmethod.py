from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
if TYPE_CHECKING:
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_method_is_classmethod(
    raw_method: Any,
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that a class attribute is explicitly decorated with @classmethod.

    Assumes that the attribute's existence within the class namespace has already been verified.

    Raises:
        SimpleMetadataError: If the raw attribute is not an instance of the classmethod descriptor.
    """

    # 1. Structural evaluation checkpoint
    if not isinstance(raw_method, classmethod):

        # 2. Extract shared diagnostic elements from context dictionary
        class_name = base_info["class_name"]
        method_name = base_info["method_name"]
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Missing classmethod decorator",
            expected="Method explicitly decorated with '@classmethod'.",
            problem=f"'{class_name}.{method_name}' is missing this decorator.",
            context=context,
            how_to_fix=(
                f"Add the '@classmethod' decorator to the '{method_name}' method.",
                "Without this decorator, the system cannot correctly evaluate its runtime parameters."
            ) + expected_structure,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_method_is_classmethod

## Purpose
Enforces descriptor requirements by ensuring that the reflected user hook is explicitly wrapped as a `classmethod`. This is critical because the framework relies on class-bound execution semantics and bytecode signature reflection that are only valid when operating on a classmethod descriptor wrapper.

## Diagnostic Layout & Formatting
1. **Dictionary Integration**: Resolves context variables (`class_name`, `method_name`) from the shared `base_info` payload map. It targets the `"expected_structure"` tracking key to inject the copy-pasteable structure layout into the remediation text.
2. **Descriptor-Level Inspection**: Inspects the raw namespace object using `isinstance(raw_method, classmethod)`. This ensures that standard instance methods or static fields are caught before they break downstream frame manipulation steps.
3. **Happy Path Performance**: Employs a single `isinstance` type check. If the hook is correctly decorated, it returns instantly, avoiding all text interpolation, dictionary lookups, and exception allocations.
"""