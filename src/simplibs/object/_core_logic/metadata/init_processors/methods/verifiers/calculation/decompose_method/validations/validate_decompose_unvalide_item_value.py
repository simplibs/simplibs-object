from typing import Any, TYPE_CHECKING
# Outers
from .........exceptions import SimpleMetadataError
from ...._exceptions_helpers import exception_context_for_classmethod
# Annotations
if TYPE_CHECKING:
    from .........protocols.methods import ClassMethodProtocol
    from .........protocols.classes import SimpleClassLike


def validate_decompose_unvalide_item_value(
    value: Any,
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    bound_method: "ClassMethodProtocol",
) -> None:
    """Validates that an item returned by the _decompose method matches its configured default blueprint value.

    Raises:
        SimpleMetadataError: If the decomposed value does not equal the expected default value.
    """

    # 1. Structural evaluation checkpoint
    if value != inner.meta.default:

        # 2. Extract shared diagnostic elements and compute default value maps
        class_name, method_name, context = exception_context_for_classmethod(bound_method)
        meta = inner.meta
        inner_values = tuple(inner.meta.default for inner in inners)

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Invalid item value in return value",
            expected=f"Value '{meta.default!r}' (as defined in '{meta.class_name}').",
            value=value,
            problem=f"Item '{meta.name_snake}' does not match the default value defined in '_inners'.",
            context=context,
            how_to_fix=(
                f"Check the value computation or mapping of item '{meta.name_snake}' inside the '_decompose' method.",
                f"Expected value is '{meta.default!r}', but received '{value!r}'.",
                "Ensure that the structural order of the returned elements strictly matches the '_inners' definition sequence.",
                f"Expected item order: '{', '.join(meta.inners_params_name)}'.",
                "Example based on default values from inners:",
                f"    return ({', '.join(map(repr, inner_values))})"
            ),
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_decompose_unvalide_item_value

## Purpose
Enforces strict value invariance assertions on structural data fields unbundled during the `_decompose` workflow. This ensures that calculated defaults or structure templates exactly match their configured default layouts before initialization pipelines lock the state.

## Diagnostic Layout & Formatting
1. **Dynamic Blueprint Mapping**: Resolves dynamic field descriptors (`name_snake`, `class_name`, `default`, `inners_params_name`) using the internal `inner.meta` schema layer to construct direct contextual hints.
2. **Representation Layer Safety**: Uses `map(repr, inner_values)` and explicit structural representation literal strings (`!r`) to ensure accurate token strings are printed for raw types (e.g. distinguishing strings from integers).
3. **Happy Path Performance**: Bypasses string building and exception mapping allocations entirely by using a standard native inequality block check (`!=`). If the dynamic value matches the preset blueprint value, execution exits instantly.
"""