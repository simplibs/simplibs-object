from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance import AtomInstanceProtocol, CompositeInstanceProtocol


def _get_inner_instance_class(
    inner_meta: "SimpleMetadataLike",
    mutable: bool,
) -> "AtomInstanceProtocol | CompositeInstanceProtocol":
    """Returns the correct instance class for an inner element."""

    # 1. Mutable branch
    if mutable:
        return (
            inner_meta.atom_class_mutable
            if inner_meta.is_constant
            else inner_meta.composite_class_mutable
        )

    # 2. Immutable branch
    return (
        inner_meta.atom_class_immutable
        if inner_meta.is_constant
        else inner_meta.composite_class_immutable
    )



_DESIGN_NOTES = """
# _get_inner_instance_class

## Purpose
Resolves the correct instance class for an inner element based on:
- mutability (mutable vs immutable)
- structural identity (constant vs composite)

## Behavior
1. If the composite instance is mutable:
   - constants use `atom_class_mutable`
   - composites use `composite_class_mutable`
2. If immutable:
   - constants use `atom_class_immutable`
   - composites use `composite_class_immutable`

## Notes
This helper isolates the resolution matrix from the composite builder.  
It also triggers lazy class creation defined on metadata, ensuring efficient
runtime behavior even for deeply nested composition trees.
"""