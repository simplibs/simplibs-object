from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_only_types_invalid(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when the '_only_types' flag is defined but does not match
    any of the supported structural forms.
    """

    only_types = cls.__dict__["_only_types"]

    raise SimpleLogicError(
        error_name="MIXIN DEFINITION ERROR",
        label="_only_types",
        expected="UNSET, type, tuple[type, ...], or UnionType.",
        value=only_types,
        problem=(
            f"Mixin '{cls.__name__}' defines '_only_types' using an unsupported value:",
            f"• {only_types!r} (type: {type(only_types).__name__})",
            "This value does not match any of the allowed structural forms.",
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Use one of the supported forms for '_only_types':",
            "UNSET",
            "a single type (e.g., int)",
            "a tuple of types (e.g., (int, float))",
            "a UnionType (e.g., int | float)",
            "If the flag is not needed, remove it from the mixin.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_only_types_invalid

## Purpose
Validates the structural correctness of the `_only_types` declarative flag.
This flag restricts mixin applicability based on the type of the underlying
value stored inside an instance. It must always match one of the supported
structural forms:

- `UNSET`
- a single type (e.g., `int`)
- a flat tuple of types (e.g., `(int, float)`)
- a modern UnionType (e.g., `int | float`)

## Architectural reasoning
The `_only_types` flag is used during instance creation to ensure that a mixin
is applied only to instances whose default value type matches the declared
constraints. Incorrect definitions (lists, dicts, objects, nested tuples)
would break:

- type compatibility checks,
- mixin applicability validation,
- instance creation determinism.

Therefore, strict structural validation is required.

## Self-contained error logic
The main validation pipeline (`verify_mixin_definition`) remains clean and
minimal. If `_only_types` is present and invalid, the pipeline delegates to
this error function.

The error function:

1. re-reads `_only_types` from the class dictionary,
2. determines the invalid structural form,
3. raises a structured diagnostic error.

This keeps the pipeline simple while the error function handles all
diagnostic responsibilities.

## Diagnostic value
The error message includes:

- the invalid value,
- its type,
- a list of all supported structural forms,
- actionable guidance for correction.

This makes debugging fast, friendly, and predictable.

## Pipeline position
This check occurs after validating:

1. `__slots__`,
2. slot types,
3. forbidden slot names,
4. mixin flags.

It is the sixth structural check in `verify_mixin_definition`.

## Notes
- This is a pure `raise_...` function.
- It is used exclusively by the mixin definition validator.
- All mixins must pass this check before they can be applied to instances.
"""

