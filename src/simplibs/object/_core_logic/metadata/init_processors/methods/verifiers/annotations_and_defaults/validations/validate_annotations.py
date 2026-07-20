from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Inners
from ._convert_annotation_to_type_set import _convert_annotation_to_type_set
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_annotations(
    bound_method_annotations: dict[str, type],
    bound_method: "ClassMethodProtocol",
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that a method parameter or return value type annotation matches the expected type (or its valid subset).

    Raises:
        SimpleMetadataError: If a defined type annotation does not conform to the expected schema layout.
    """

    # 1. Extract explicitly declared user annotations from the target method
    method_annotations = bound_method.__func__.__annotations__ or {}

    # 2. If the user provided no explicit type annotations, exit immediately (Happy Path)
    if not method_annotations:
        return

    # 2. Validation block execution
    if method_annotations:

        # 2.1 Iterate through each declared annotation entry
        for name, annotation in method_annotations.items():

            # 2.2 Resolve expected annotation schema
            # (Converts types to sets to handle UnionType variations seamlessly)
            expected_type = bound_method_annotations.get(name)
            expected_type_set = _convert_annotation_to_type_set(expected_type)
            annotation_set = _convert_annotation_to_type_set(annotation)

            # 2.3 Verify if the declared type set is a strict variant subset of the blueprint
            if not annotation_set.issubset(expected_type_set):

                # 2. Extract shared pre-computed diagnostic elements from base payload
                expected_structure = base_info["expected_structure"]
                context = base_info["context"]
                expected_names = " | ".join(t.__name__ for t in expected_type_set)
                annotation_names = " | ".join(t.__name__ for t in annotation_set)

                # 3. Raise domain exception with full packed diagnostic payload
                raise SimpleMetadataError(
                    error_name="METHOD SIGNATURE ERROR",
                    label="Invalid type annotation",
                    expected=f"Type annotation matching '{expected_names}'.",
                    problem=f"The defined annotation '{annotation_names}' does not conform to the expected blueprint.",
                    context=context,
                    how_to_fix=(
                        f"Modify the annotation in the method definition to align with '{expected_names}'.",
                        "The annotation must be of the exact same type or a valid operational subtype (subset).",
                        "Alternatively, remove the type annotation from the method signature entirely;",
                        "the framework will automatically inject it during metadata initialization.",
                    ) + expected_structure,
                    exception=TypeError
                )


_DESIGN_NOTES = """
# validate_annotations

## Purpose
Enforces variance constraints on user-declared method signatures. By mapping runtime annotations to comprehensive type sets, it enables flexible union typing while ensuring that user-facing code hints never break the engine's core internal processing requirements.

## Diagnostic Layout & Formatting
1. **Set-Based Variance Resolution**: Uses `_convert_annotation_to_type_set` to normalize native types, pipe combinations, and `UnionType` constructs into consistent standard set footprints, evaluating type safety via variance subset checks (`issubset`).
2. **Dynamic Union Serialization**: Joins resolved type tags dynamically via `" | "` delimiters, recreating standard PEP 604 type layout syntax inside error outputs even when unpacking complex nested values.
3. **Happy Path Performance**: Shields parsing tasks from slow dictionary iterations and type normalization conversions by executing a short-circuit boundary check on `method_annotations` right at entry.
"""