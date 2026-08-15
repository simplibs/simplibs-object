from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.instance.core_classes import AtomInstanceProtocol, CompositeInstanceProtocol


def get_base_class(
    cls: "SimpleClassLike",
    is_atom: bool,
    mutable: bool,
) -> "AtomInstanceProtocol | CompositeInstanceProtocol":
    """Returns the correct base instance class based on structural mode and mutability."""

    # 1. Atomic branch
    if is_atom:
        return (
            cls.meta.atom_class_mutable
            if mutable else
            cls.meta.atom_class_immutable
        )

    # 2. Composite branch
    return (
        cls.meta.composite_class_mutable
        if mutable else
        cls.meta.composite_class_immutable
    )



_DESIGN_NOTES = """
# get_base_class

## Purpose
Resolves the correct runtime base class for a new instance.  
This determines the entire structural behavior of the instance: slots, init pipeline,
reactive methods, and memory layout.

## Behavior
1. If the instance is atomic:
   - returns `atom_class_mutable` or `atom_class_immutable`
2. If the instance is composite:
   - returns `composite_class_mutable` or `composite_class_immutable`

## Notes
- This function is the structural routing gate of the instance‑builder.
- Delegates fully to metadata (`cls.meta`), which handles lazy compilation and caching.
- Guarantees deterministic selection across two orthogonal axes:
  - **Topology:** atom vs composite  
  - **Mutability:** mutable vs immutable  
- Keeps the instance‑builder minimal and avoids branching duplication.
"""