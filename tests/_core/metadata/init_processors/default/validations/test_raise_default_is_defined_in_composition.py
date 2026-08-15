from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_default import _exception_info_for_default
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def raise_default_is_defined_in_composition(
    owner_class: "SimpleClassLike"
) -> None:
    """Raises an error when a composite defines '_default'."""

    (
        class_name,
        class_parent,
        error_name,
        context,
    ) = _exception_info_for_default(owner_class)

    raise SimpleMetadataError(
        error_name=error_name,
        label="_default",
        problem=(
            f"The composite class '{class_name}' defines '_default', which is forbidden.",
        ),
        expected="A composite class without '_default'.",
        how_to_fix=(
            "Remove '_default' from the class definition.",
            "Composite objects compute their value via '_inners' and '_logic'.",
            "If this class is meant to be a constant, remove '_inners' and '_logic'.",
        ),
        context=context,
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_default_is_defined_in_composition

## Purpose
Blocks composite objects (`SimpleObject`) from defining `_default`.  
Composites compute their value dynamically from:

- `_inners` (structure),
- `_logic` (aggregation).

A manual `_default` would bypass this mechanism and break determinism.

## Why this validation exists
Composite objects represent structured data.  
Their default state is derived from the defaults of their inner components.  
If a composite defined `_default`, it would create:

- two competing sources of truth,
- unpredictable initialization,
- broken metadata consistency.

Therefore `_default` is strictly forbidden.

## Pipeline position
This guard is executed inside `SimpleObjectMetadata._process_user_data`.  
It runs before inner fields are processed, ensuring early detection.

## Developer experience
The error message clearly explains:

- why `_default` is forbidden,
- how to fix the class,
- how to convert the class into a constant if that was the intention.

## Notes
This validator is used only for compositions.  
Constants use `process_default_for_constant` instead.

"""