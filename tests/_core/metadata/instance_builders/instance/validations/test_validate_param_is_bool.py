# Outers
from ......exceptions import SimpleInstanceError


def validate_param_is_bool(
    as_atom: bool,
) -> None:
    """Validates that a parameter is of type bool."""

    # 1. Check type
    if isinstance(as_atom, bool):
        return

    # 2. Raise error
    raise SimpleInstanceError(
        error_name="INVALID PARAMETER",
        label="param_not_bool",
        expected="Boolean value (True or False)",
        value=as_atom,
        problem=f"Parameter is not bool. Received: {as_atom!r} ({type(as_atom).__name__}).",
        context="create_instance(..., as_atom=...)",
        how_to_fix=(
            "Set the parameter to True or False.",
            "Example:",
            "    create_instance(MyClass, mixins=(), as_atom=True)",
        ),
        exception=TypeError,
    )


_DESING_NOTES = """
# validate_param_is_bool

## Purpose
Ensures that boolean configuration parameters (`as_atom`, `mutable`) are strictly
typed as `bool`. Prevents silent coercion or accidental misuse of truthy/falsy
values.

## Behavior
1. Checks whether the parameter is an instance of `bool`.
2. If not, raises `SimpleInstanceError` with a clear remediation message.

## Notes
- Boolean flags control structural behavior (atomic vs composite, mutable vs immutable).
- Accepting non-boolean values would break determinism in the instance‑builder pipeline.
- This validator is used early to guarantee predictable branching logic.
"""