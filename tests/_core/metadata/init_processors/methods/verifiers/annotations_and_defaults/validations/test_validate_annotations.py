from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Inners
from ._convert_annotation_to_type_set import _convert_annotation_to_type_set
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def validate_annotations(
    bound_method_annotations: dict[str, type],
    bound_method: "ClassMethodProtocol",
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that user-declared type annotations match expected types."""

    # 1. Extract user annotations
    method_annotations = bound_method.__func__.__annotations__ or {}

    # 2. Happy path: no annotations declared
    if not method_annotations:
        return

    class_name, method_name, context = exception_info

    # 3. Validate each annotation
    for name, annotation in method_annotations.items():
        expected_type = bound_method_annotations.get(name)

        expected_type_set = _convert_annotation_to_type_set(expected_type)
        annotation_set = _convert_annotation_to_type_set(annotation)

        # 4. Check subset relationship
        if not annotation_set.issubset(expected_type_set):
            expected_names = " | ".join(t.__name__ for t in expected_type_set)
            annotation_names = " | ".join(t.__name__ for t in annotation_set)

            raise SimpleMetadataError(
                error_name="METHOD SIGNATURE ERROR",
                label="_annotation",
                value=annotation_names,
                expected=expected_names,
                problem=f"Annotation for '{name}' does not match expected types.",
                context=context,
                how_to_fix=(
                    f"Change the annotation to match '{expected_names}'.",
                    "The annotation must be the same type or a valid subset.",
                    "You may also remove the annotation entirely; the framework will inject it automatically.",
                ) + expected_structure,
                exception=TypeError,
            )


_DESIGN_NOTES = """
# validate_annotations

## Purpose
Ensures that user-declared type annotations match the expected types defined by
the metadata pipeline.  
Annotations are normalized into sets so that union types can be compared using
simple subset logic.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method-validation helpers.

## Behavior
1. Extract user annotations.
2. If none exist → exit immediately.
3. Convert both expected and actual annotations into type sets.
4. Check whether the actual set is a subset of the expected set.
5. If not, raise a structured `SimpleMetadataError` with a copy-paste blueprint.

## Notes
This validator is part of the annotation/defaults verification chain:
- `validate_annotations`
- `validate_args_defaults`
- `validate_kwargs_defaults`
"""