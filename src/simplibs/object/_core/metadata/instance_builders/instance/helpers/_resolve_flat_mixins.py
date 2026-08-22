from typing import TYPE_CHECKING
# Inners
from ._verify_mixin_compatibility import _verify_mixin_compatibility
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.alias_typings import MixinsTuple


def _resolve_flat_mixins(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    is_atom: bool,
    mutable: bool,
) -> tuple:
    """Unrolls all mixins and their parents into a unique, flattened list while validating each node."""

    # 1. Local import to avoid circular dependencies
    from ......mixins.base_class import SimpleMixin

    # 2. Use dict keys as an O(1) insertion-ordered set
    flat_mixins = {}

    # 3. Iterate through top-level mixins
    for mixin in mixins:

        # 3.1 Traversal over mixin ancestry (MRO)
        for mro_mixin in mixin.__mro__:

            # 3.2 Filter out generic base roots
            if mro_mixin not in (object, SimpleMixin):

                # 3.3 Process unvisited mixin node
                if mro_mixin not in flat_mixins:

                    # 3.4 Validate individual mixin compatibility
                    _verify_mixin_compatibility(cls, mro_mixin, is_atom, mutable)

                    # 3.5 Mark as visited
                    flat_mixins[mro_mixin] = True

    # 4. Return immutable tuple of resolved mixins
    return tuple(flat_mixins.keys())


_DESIGN_NOTES = """
# _resolve_flat_mixins

## Purpose
Flattens a tuple of top-level user mixins and their full inheritance trees (MRO) into a 
deduplicated, order-preserving tuple of mixin classes, validating each individual node.

## Pipeline & Logic
1. **Local Import Optimization**
   Imports `SimpleMixin` locally to avoid circular import issues with the core mixin hierarchy.

2. **O(1) Deduplication via Dict Keys**
   Employs a Python dictionary as an insertion-ordered set. Checking `mro_mixin not in flat_mixins`
   is an $O(1)$ operation while preserving strict linear resolution order.

3. **Ancestry Unrolling (`__mro__`)**
   Traverses every ancestor class of each provided mixin to collect inherited mixin logic.
   Filters out root primitives (`object`, `SimpleMixin`).

4. **In-Flight Validation (`_verify_mixin_compatibility`)**
   Validates every discovered mixin class against structural and context constraints 
   (e.g., `_constant_only`, `_mutable_only`, type compatibility) before registering it.

## Architectural Notes
- **Order Preservation**: Unrolling order is crucial because `_build_instance_class_dict` 
  iterates over the resulting tuple in reverse to ensure proper attribute override semantics.
- **Eager Validation**: Validating mixins during the flattening phase ensures that invalid 
  mixins deep inside an MRO are caught early, before class construction begins.
"""