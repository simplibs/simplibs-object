from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_method_is_defined(
    method_name: str,
    owner_class: "SimpleClassLike",
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that a specific method is explicitly defined on the class level.

    Checks directly within the class __dict__ to ensure that the subclass has implemented
    the method instead of inheriting a default stub or fallback implementation.

    Raises:
        SimpleMetadataError: If the method is not found directly within the class __dict__.
    """

    # 1. Structural evaluation checkpoint
    if method_name not in owner_class.__dict__:

        # 2. Extract shared diagnostic elements from context dictionary
        class_name = base_info["class_name"]
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Missing method definition",
            expected=f"Class method '{method_name}()'.",
            problem=f"Class '{class_name}' is missing this method definition.",
            context=context,
            how_to_fix=(
                f"Add the method '{method_name}' directly to the definition of class '{class_name}'.",
                "The method must be explicitly decorated with '@classmethod'.",
                "Ensure its signature parameters match the defined '_inners' configuration."
            ) + expected_structure,
            exception=AttributeError
        )


_DESIGN_NOTES = """
# validate_method_is_defined

## Purpose
Enforces explicit subclass implementation boundaries for framework hooks. By bypassing standard attribute resolution (`hasattr`) and checking `owner_class.__dict__` directly, the framework guarantees that a developer has actually provided a custom implementation rather than silently relying on an empty parent base hook.

## Diagnostic Layout & Formatting
1. **Dictionary Integration**: Resolves context formatting keys (`class_name`) from the shared `base_info` tracking payload. It utilizes the `"expected_structure"` tracking token to append the structured code layout string directly to the remediation steps.
2. **Local Namespace Guarding**: Isolates the validation to the localized class dictionary namespace. This prevents false positives from inherited lookup paths before bytecode metadata extraction begins.
3. **Happy Path Performance**: Uses a highly optimized native dictionary membership test (`in`). If the method key is defined locally, the validation returns instantly with no lookup overhead or diagnostic payload resolution.
"""