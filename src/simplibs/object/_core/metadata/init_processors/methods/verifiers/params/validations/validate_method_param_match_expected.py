# Outers
from ........exceptions import SimpleDefinitionError


def validate_method_param_match_expected(
    method_params: tuple[str, ...],
    expected_params: tuple[str, ...],
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that parameter names and order match expectations."""

    if method_params != expected_params:
        class_name, method_name, context = exception_info

        raise SimpleDefinitionError(
            error_name="METHOD SIGNATURE ERROR",
            label="_params",
            value=method_params,
            expected=repr(expected_params),
            problem="Parameter names or their order do not match the expected signature.",
            context=context,
            how_to_fix=(
                "Adjust the method signature to match the expected parameter layout.",
                "The first parameter must always be 'cls'.",
                "All other parameters must match the snake_case names of '_inners' components.",
            ) + expected_structure,
            exception=TypeError,
        )


_DESIGN_NOTES = """
# validate_method_param_match_expected

## Purpose
Ensures that the method signature parameters match the expected names and order.
This is critical because the metadata pipeline binds parameters directly to
`_inners` components.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method‑validation helpers.

## Behavior
The function performs a strict tuple comparison:
- same number of parameters,
- same names,
- same order.

If any part differs, a structured `SimpleDefinitionError` is raised with a
copy‑paste ready blueprint showing the correct method layout.

## Notes
This validator is part of the parameter‑verification chain:
- `validate_method_param_match_expected`
- `validate_method_has_exact_args_count`
- `validate_method_not_use_param_placeholders`
"""