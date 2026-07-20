from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Inners
from ._get_collision_path import _get_collision_path
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_collision_within_inners(
    collision_name: str,
    owner_snake_name: str,
    raw_inners: tuple["SimpleClassLike", ...],
    current_inner: "SimpleClassLike",
    owner_class: "SimpleClassLike"
) -> None:
    """Identifies the root cause of a name collision between sibling inner elements and raises a detailed error trace."""

    # 1. Exception condition
    if collision_name and collision_name != owner_snake_name:

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Locate the path to the first culprit (the component that registered the name first)
        first_culprit_path = None
        for previous_inner in raw_inners:
            if collision_name in previous_inner.meta.node_names_set:
                first_culprit_path = _get_collision_path(previous_inner, collision_name)
                break
        first_culprit_full_path = f"{class_name} -> {first_culprit_path}"

        # 4. Locate the path to the second culprit (the current component introducing the duplicate)
        second_culprit_path = _get_collision_path(current_inner, collision_name)
        second_culprit_full_path = f"{class_name} -> {second_culprit_path}"

        # 5. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Name collision detected within _inners",
            expected="Unique identifier names (name_snake) for all components across the composition tree.",
            problem="A naming conflict was discovered between two or more elements nested within the composition.",
            context=context,
            how_to_fix=(
                f"Conflicting name identifier: '{collision_name}'.",
                f"Path to the existing definition: {first_culprit_full_path}.",
                f"Path to the duplicate declaration: {second_culprit_full_path}.",
                f"Rename one of the conflicting components so it resolves to a unique name within '{class_name}'.",
                "Ensure you haven't accidentally registered the exact same class multiple times inside the '_inners' tuple.",
                "Note: 'name_snake' is derived directly from the class name and must remain globally unique within this composition tree.",
            ),
            exception=NameError
        )


_DESIGN_NOTES = """
# validate_collision_within_inners

## Purpose
This validation acts as a precision diagnostic tool. It is triggered only when a name duplicate 
has been verified within the sibling components collection (`_inners`), and collisions with the 
root owner class have already been cleared. Its primary goal is to inspect the `_inners` pipeline 
and build a visual breadcrumb trail locating the original and conflicting declarations.

## Culprit Identification Strategy
Since `_inners` is an ordered, immutable tuple, the validation walks the structure in the exact sequence 
it was declared. By using `get_collision_path`, it performs deep recursive lookups using `node_names_set` 
pre-filtering. This reliably isolates both the original component that first reserved the snake name 
and the new incoming component attempting to overwrite it.

## Architectural Design & Semantics
Unlike standard validators that conditionally pass or fail, this function is an absolute enforcement barrier. 
If the execution flow reaches this module, a terminal conflict state is guaranteed, and a structured `NameError` 
is always raised. Delegating this heavy tracing logic to a dedicated module keeps the main iteration compiler 
loop extremely clean, fast, and readable.
"""