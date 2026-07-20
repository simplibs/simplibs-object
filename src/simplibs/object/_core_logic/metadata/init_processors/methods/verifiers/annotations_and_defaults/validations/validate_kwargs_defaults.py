from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_kwargs_defaults(
    expected_kwargs_defaults: dict[str, Any],
    bound_method: "ClassMethodProtocol",
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that if a user defined default values in a method signature, they strictly match the values defined in '_inners'.

    In the Simple framework, composition is completely deterministic. Default values
    for business logic are fixed by the object's structural blueprint. User definitions
    in the signature serve only as documentation and IDE type-hinting support, and
    must never alter core engine logic.

    Raises:
        SimpleMetadataError: If any explicitly defined keyword default value mismatches the blueprint schema.
    """

    # 1. Extract explicitly declared user defaults from the target method
    # (Inspecting __kwdefaults__ since all framework interaction parameters are Keyword-Only)
    method_kwargs_defaults = bound_method.__func__.__kwdefaults__ or {}

    # 2. If the user provided no signatures defaults, exit immediately (Happy Path)
    if not method_kwargs_defaults:
        return

    # 3. Iterate over signature parameters and verify structural invariance
    for name, value in method_kwargs_defaults.items():

        # 3.1 Fetch the expected blueprint default value
        expected_value = expected_kwargs_defaults.get(name)

        # 3.2 Evaluate identity and equality constraints
        if value != expected_value:

            # 3.2.1 Extract shared pre-computed diagnostic elements from base payload
            expected_structure = base_info["expected_structure"]
            context = base_info["context"]

            # 3.2.2 Raise domain exception with full packed diagnostic payload
            raise SimpleMetadataError(
                error_name="METHOD SIGNATURE ERROR",
                label="Invalid keyword argument default value",
                expected=f"Value '{expected_value}' (as defined in '_inners')",
                value=value,
                problem=f"Parameter '{name}' does not conform to the expected blueprint default value.",
                context=context,
                how_to_fix=(
                    f"Align the default value of parameter '{name}' with its definition inside '_inners'.",
                    f"Recommended value: {repr(expected_value)}",
                    "Alternatively, remove the default value from the method signature entirely;",
                    "the framework will automatically inject the configured default during metadata compilation.",
                ) + expected_structure,
                exception=ValueError
            )


_DESIGN_NOTES = """
# validate_kwargs_defaults

## Purpose
Enforces deterministic design principles across method definitions by checking keyword-only signature defaults (`__kwdefaults__`) against internal blueprint data schemas. It guarantees that user-facing IDE documentation helpers remain synchronous with underlying object graph composition layouts.

## Diagnostic Layout & Formatting
1. **Shared State Re-use**: Avoids local framework introspection duplication by extracting pre-computed diagnostic structures (`expected_structure` tuple and `context` marker) directly from the incoming `base_info` payload block.
2. **Tuple Chaining Layout**: Dynamically appends the contextual code-structure representation strings by unpacking and concatenating `expected_structure` right into the `how_to_fix` diagnostic tuple.
3. **Happy Path Performance**: Optimizes core initialization performance by executing a direct evaluation boundary check on `method_kwargs_defaults`. If no keyword arguments specify explicit default initializers, execution drops out instantly without allocating string maps or triggering loops.
"""