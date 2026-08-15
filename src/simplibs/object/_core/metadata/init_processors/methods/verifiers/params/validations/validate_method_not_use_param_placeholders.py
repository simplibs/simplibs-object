# Outers
from ........exceptions import SimpleDefinitionError


def validate_method_not_use_param_placeholders(
    has_varargs: bool,
    has_varkwargs: bool,
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that *args and **kwargs are not used in the method signature."""

    if has_varargs or has_varkwargs:
        class_name, method_name, context = exception_info

        tokens = []
        if has_varargs:
            tokens.append("*args")
        if has_varkwargs:
            tokens.append("**kwargs")

        joined = ", ".join(tokens)

        raise SimpleDefinitionError(
            error_name="METHOD SIGNATURE ERROR",
            label="_params",
            value=joined,
            expected="Explicitly named parameters.",
            problem=f"'{class_name}.{method_name}' uses prohibited placeholders: {joined}.",
            context=context,
            how_to_fix=(
                f"Remove '{joined}' from the method signature.",
                "Declare each parameter explicitly by its exact semantic name.",
            ) + expected_structure,
            exception=TypeError,
        )


_DESIGN_NOTES = """
# validate_method_not_use_param_placeholders

## Purpose
Ensures deterministic method signatures by forbidding `*args` and `**kwargs`.
Every parameter must be explicitly named and mapped to a specific semantic role.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method‑validation helpers.

## Behavior
The function checks bytecode flags:
- `has_varargs` → presence of `*args`
- `has_varkwargs` → presence of `**kwargs`

If either is present, a structured `SimpleDefinitionError` is raised with a clear
explanation and a copy‑paste ready blueprint.

## Notes
This validator is part of the parameter‑verification chain:
- `validate_method_param_match_expected`
- `validate_method_has_exact_args_count`
- `validate_method_not_use_param_placeholders`
"""