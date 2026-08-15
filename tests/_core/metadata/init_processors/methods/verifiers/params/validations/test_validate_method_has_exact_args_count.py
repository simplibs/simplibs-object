# Outers
from ........exceptions import SimpleMetadataError


def validate_method_has_exact_args_count(
    expected_args_count: int,
    actual_args_count: int,
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that the positional argument count matches expectations."""

    if actual_args_count != expected_args_count:
        class_name, method_name, context = exception_info

        raise SimpleMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            label="_args_count",
            value=actual_args_count,
            expected=str(expected_args_count),
            problem="Incorrect number of positional arguments.",
            context=context,
            how_to_fix=(
                "Ensure all required positional parameters are declared after 'cls'.",
                "Verify that the classmethod signature matches the expected framework definition.",
            ) + expected_structure,
            exception=TypeError,
        )



_DESIGN_NOTES = """
# validate_method_has_exact_args_count

## Purpose
Ensures that the number of positional arguments in the method signature matches
the expected count derived from the metadata pipeline.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method‑validation helpers.

## Behavior
The function compares:
- `actual_args_count` (from bytecode `co_argcount`)
- `expected_args_count` (from metadata)

If they differ, a structured `SimpleMetadataError` is raised with a clear
explanation and a copy‑paste ready blueprint.

## Notes
This validator is part of the parameter‑verification chain:
- `validate_method_param_match_expected`
- `validate_method_has_exact_args_count`
- `validate_method_not_use_param_placeholders`
"""