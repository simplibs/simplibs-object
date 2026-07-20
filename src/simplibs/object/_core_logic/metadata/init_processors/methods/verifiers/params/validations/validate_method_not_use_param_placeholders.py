from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_method_not_use_param_placeholders(
    has_varargs: bool,
    has_varkwargs: bool,
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that the classmethod signature does not contain variable placeholder arguments (*args or **kwargs).

    Raises:
        SimpleMetadataError: If either variable positional or keyword placeholders are detected.
    """

    # 1. Structural evaluation checkpoint
    if has_varargs or has_varkwargs:

        # 2. Extract shared diagnostic elements from context dictionary
        class_name = base_info["class_name"]
        method_name = base_info["method_name"]
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # Identify violating structural components for localized logging
        problem_tokens = []
        if has_varargs:
            problem_tokens.append("*args")
        if has_varkwargs:
            problem_tokens.append("**kwargs")

        joined_tokens = ", ".join(problem_tokens)

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            label="Prohibited variable parameters",
            expected="Explicitly named parameters mapping to specific semantic domain values.",
            problem=f"The method '{class_name}.{method_name}' utilizes prohibited parameter placeholders: {joined_tokens}.",
            context=context,
            how_to_fix=(
                f"Remove the '{joined_tokens}' placeholder from the method signature declaration.",
                "Explicitly declare every expected parameter individually by its exact semantic name."
            ) + expected_structure,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_method_not_use_param_placeholders

## Purpose
Enforces deterministic signature layouts by explicitly banning generic variable argument collections (`*args`, `**kwargs`) inside core framework classmethods. Every parameter must be statically and semantically declared.

## Implementation & Type Safety
1. **Linter Type Enforcement**: Implements an inline type annotation overlay (`expected_structure: tuple[str, ...]`) to guarantee the type-checker safely compiles the tuple concatenation operator (`+`).
2. **Dynamic Violation Mapping**: Evaluates bytecode flags (`0x04` and `0x08`) compiled into `has_varargs` and `has_varkwargs`. It builds accurate diagnostic descriptions indicating exactly which dynamic tokens violated the contract.
3. **Performance Optimization**: Bypasses dictionary extractions, list instantiations, and string joins completely if the method passes the initial boolean evaluation layer.
"""