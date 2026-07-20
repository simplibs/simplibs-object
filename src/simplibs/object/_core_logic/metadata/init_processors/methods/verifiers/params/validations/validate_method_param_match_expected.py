from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_method_param_match_expected(
    method_params: tuple[str, ...],
    expected_params: tuple[str, ...],
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that the parameter names and their exact sequence match the framework expectations.

    Raises:
        SimpleMetadataError: If the actual parameter signature names deviate from the expected configuration.
    """

    # 1. Structural evaluation checkpoint
    if method_params != expected_params:

        # 2. Extract shared diagnostic elements from context dictionary
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            label="Parameter layout mismatch",
            expected=f"{repr(expected_params)} (tuple)",
            value=method_params,
            problem="The declared signature parameters do not match the expected specification layout.",
            context=context,
            how_to_fix=(
                "Adjust the method definition signature so that every parameter exactly matches expectations.",
                "The very first signature parameter token must always be declared as 'cls'.",
                "The names of subsequent parameters must strictly match the snake_case identifiers of your '_inners' components.",
            ) + expected_structure,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_method_param_match_expected

## Purpose
Enforces strict name compliance and declaration ordering across method signature parameters. It guarantees that the arguments mapped via bytecode align identically with the target orchestrator contract.

## Design Decisions & Layout
1. **Strict Sequence Matching**: The function evaluates both identity and positions of the parameter strings via direct tuple inequality (`!=`). This blocks swapped positions even if the total argument count is correct.
2. **Framework Alignment Rules**: The remediation directives explicitly highlight the core requirements: forcing the initial `cls` boundary token and forcing all trailing parameters to bind directly to the snake_case identities of the corresponding system `_inners`.
3. **Type-Checker Overlay**: Integrates the `expected_structure: tuple[str, ...]` inline hint layer to ensure seamless string/tuple collection merging without static diagnostic alerts.
"""