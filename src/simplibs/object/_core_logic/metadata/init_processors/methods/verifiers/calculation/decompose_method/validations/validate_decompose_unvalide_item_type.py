from typing import Any, TYPE_CHECKING
from types import UnionType
# Outers
from .........exceptions import SimpleMetadataError
from ...._exceptions_helpers import exception_context_for_classmethod

# Annotations
if TYPE_CHECKING:
    from .........protocols.methods import ClassMethodProtocol
    from .........protocols.classes import SimpleClassLike


def validate_decompose_unvalide_item_type(
    value: Any,
    expected_type: type | UnionType,
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    bound_method: "ClassMethodProtocol",
) -> None:
    """Validates that each item returned by the _decompose method matches its expected inner configuration type.

    Raises:
        SimpleMetadataError: If the decomposed value is not an instance of the expected type.
    """

    # 1. Structural evaluation checkpoint
    if not isinstance(value, expected_type):
        # 2. Extract shared diagnostic elements and compute fallback typenames
        class_name, method_name, context = exception_context_for_classmethod(bound_method)
        meta = inner.meta
        inner_values = tuple(repr(i.meta.default) for i in inners)

        # Safely extract name for standard types or use string representation for UnionType
        expected_type_name = expected_type.__name__ if hasattr(expected_type, "__name__") else str(expected_type)

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Invalid item type in return value",
            expected=f"Value of type '{expected_type_name}' (as defined in '{meta.class_name}').",
            value=value,
            problem=f"Item '{meta.name_snake}' is not compatible with its '_inners' configuration definition.",
            context=context,
            how_to_fix=(
                f"Check the computation or extraction of item '{meta.name_snake}' inside the '_decompose' method.",
                f"Expected type is '{expected_type_name}', but received '{type(value).__name__}'.",
                "Ensure that the structural order of the returned elements strictly matches the '_inners' definition sequence.",
                f"Expected item order: '{', '.join(meta.inners_params_name)}'.",
                "Example based on default values from inners:",
                f"    return ({', '.join(inner_values)})"
            ),
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_decompose_unvalide_item_type

## Purpose
Enforces type-safety invariants on the unpacked tuple items yielded by a custom class's `_decompose` method. It guarantees that the structural output elements structurally match their corresponding blueprint fields before downstream assignment routines occur.

## Diagnostic Layout & Formatting
1. **Dynamic Blueprint Mapping**: Resolves dynamic metadata identifiers (`name_snake`, `class_name`, `inners_params_name`) via the `inner.meta` reflection layer to render precise context-rich diagnostic traces.
2. **Union-Safe Type Introspection**: Extracts type string identifiers while keeping compatibility with both raw class constructors (`type`) and complex generic expressions (`UnionType`) without causing attribute crashes during exception generation.
3. **Happy Path Performance**: Shields execution overhead behind a highly optimized native type check (`isinstance`). If the item matches its declared schema configuration, runtime lookups and allocation routines are skipped entirely.
"""