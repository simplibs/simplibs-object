from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def _exception_info_for_type(
    owner_class: "SimpleClassLike",
) -> tuple[str, str, str, str, tuple[str, ...]]:
    """Gathers standardized diagnostic data and architectural blueprints for type-related validation exceptions."""
    attribute_name = "_type"
    class_name = owner_class.__name__
    class_parent = "SimpleObject" if "SimpleObject" in owner_class.__mro__ else "SimpleConstant"
    error_name = "INVALID TYPE DEFINITION"
    context = f"Metadata evaluation and validation for: {class_name}.{attribute_name}"

    acceptable_definitions = (
        "Acceptable definitions:",
        f"class {class_name}({class_parent}):",
        f"    {attribute_name} = int  # Atomic type definitions (e.g., str, int, float, custom classes)",
        f"    {attribute_name} = int | str  # Modern UnionType expressions for multiple allowed types",
        f"    {attribute_name} = (int, str)  # Standard tuple of types (automatically transformed into UnionType)",
        "    ...",
    )

    return class_name, class_parent, error_name, context, acceptable_definitions


_DESIGN_NOTES = """
# _exception_info_for_type

## Purpose
Acts as a centralized diagnostic registry for all validation errors occurring within 
the `_type` parsing lifecycle. It isolates string formatting and architectural 
blueprints from the operational validation logic.

## Structural Strategy
By dynamically checking the `__mro__` of the `owner_class`, it precisely identifies 
whether the target structure is a composite node (`SimpleObject`) or a terminal leaf 
(`SimpleConstant`). This allows the generated `acceptable_definitions` to present 
highly accurate, contextual code snippets directly inside the exception body.

## Code Blueprint Alignment
The generated snippets explicitly use variable assignment `=` rather than type hinting 
annotations `:`, mirroring exactly how developers are expected to define structural 
metadata attributes within the class definitions of the framework.
"""