from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def _exception_info_for_default(
    owner_class: "SimpleClassLike",
) -> tuple[str, str, str, str]:
    """Collects diagnostic data for default-value validation errors."""

    attribute_name = "_default"
    class_name = owner_class.__name__

    class_parent = (
        "SimpleObject"
        if "SimpleObject" in owner_class.__mro__
        else "SimpleConstant"
    )

    error_name = "INVALID DEFAULT DEFINITION"
    context = f"Metadata validation for: {class_name}.{attribute_name}"

    return (
        class_name,
        class_parent,
        error_name,
        context,
    )


_DESIGN_NOTES = """
# _exception_info_for_default

## Purpose
Provides shared diagnostic values for all default‑related validation errors.
This keeps validation functions clean and prevents duplication of formatting logic.

## Returned values
The helper returns four items:

1. **class_name** — name of the class being validated  
2. **class_parent** — `"SimpleObject"` or `"SimpleConstant"` depending on MRO  
3. **error_name** — fixed label for default‑related errors  
4. **context** — string describing where the error occurred  

These values are injected directly into `SimpleMetadataError`.

## Why this helper exists
Default validation appears in three places:

- constants: `_default` must exist  
- constants: `_default` must match `_type`  
- compositions: `_default` must NOT exist  

All tyto validace potřebují stejné základní diagnostické údaje.

## Notes
The helper is intentionally minimal:

- no branching logic  
- no dynamic formatting  
- no heavy structures  

It returns a fixed tuple because the data is used once and immediately unpacked.
"""