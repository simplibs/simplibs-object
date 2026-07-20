from typing import TYPE_CHECKING, Tuple

# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def _exception_info_for_inners(
    owner_class: "SimpleClassLike",
) -> Tuple[str, str, str, Tuple[str, ...]]:
    """Generates standardized diagnostic information and contextual blueprints for inner elements validation errors."""

    class_name = owner_class.__name__
    error_name = "INVALID INNERS DEFINITION"
    context = f"Metadata inspection and validation for: {class_name}._inners"

    acceptable_definitions = (
        "Acceptable definitions:",
        f"class {class_name}(SimpleObject):",
        "    _inners: tuple[type[SimpleConstant], ...] = (FirstElement, SecondElement)",
        "    ...",
    )

    return class_name, error_name, context, acceptable_definitions


_DESIGN_NOTES = """
# _exception_info_for_inners

## Purpose
Provides a centralized diagnostic data factory for all exception blocks within the 
`_inners` structural processing sub-pipeline. This guarantees absolute layout and 
semantic harmony across all validation reports.

## Architecture & Reusability
By bundling common structural components (`class_name`, `error_name`, `context`, and 
`acceptable_definitions`) into a single helper, individual validation modules do not 
need to know how to format class definitions or compute error strings. They simply 
unpack this tuple and append their specific error context.

## Maintenance Benefits
If the framework blueprint syntax changes or if the core metadata inspection layer 
requires additional attributes, changes are localized entirely to this single module, 
shielding the validation execution nodes from modification.
"""