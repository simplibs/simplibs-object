from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance import AtomInstanceProtocol, CompositeInstanceProtocol


def _get_inner_instance_class(
    inner_meta: "SimpleMetadataLike",
    mutable: bool
) -> "AtomInstanceProtocol | CompositeInstanceProtocol":
    """Internal resolution helper selecting the appropriate generated class target.

    Branches down the type definition matrix based on mutability constraints and node placement
    within the configuration graph (Constant vs Composite).
    """
    if mutable:
        return (
            inner_meta.atom_class_mutable
            if inner_meta.is_constant
            else inner_meta.composite_class_mutable
        )
    return (
        inner_meta.atom_class_immutable
        if inner_meta.is_constant
        else inner_meta.composite_class_immutable
    )


_DESIGN_NOTES = """
# _get_inner_instance_class

## Purpose
Acts as a private structural routing gate during class compilation inside the composite builder layer. It maps declarative nested member metadata configurations into concrete, compiled runtime class objects based on a strict two-dimensional resolution matrix (Mutability $\\times$ Structural Node Identity).

## Architectural Design Decisions

### 1. Separation of Concerns & Matrix Resolution
* The helper isolates the condition branching matrix from the primary orchestration pipelines of composite initialization and property attachment.
* It models type topology into two clear questions:
  1. **Is the target mutable?** (Toggles `mutable` vs `immutable` class pools).
  2. **Is the target a terminal constant?** (Toggles `atom_class` leaf objects vs `composite_class` subtree nodes).

### 2. Micro-Optimization of Lazily Compiled Targets
* By addressing properties such as `inner_meta.atom_class_mutable` or `inner_meta.composite_class_mutable`, this helper triggers the upstream lazy loading mechanics defined on the metadata block level.
* The execution cost is kept minimal through direct lookup routing, preventing compilation overhead from slowing down deep composition graphs containing heavily nested structures.
"""