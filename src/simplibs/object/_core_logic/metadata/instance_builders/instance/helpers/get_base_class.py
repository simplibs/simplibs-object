from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.instance.core_classes import AtomInstanceProtocol, CompositeInstanceProtocol


def get_base_class(
    cls: "SimpleClassLike",
    is_atom: bool,
    mutable: bool,
) -> "AtomInstanceProtocol | CompositeInstanceProtocol":
    """Returns the appropriate base instance class based on structural mode and mutability traits.

    - If the instance is atomic → selects `atom_class_mutable` or `atom_class_immutable`.
    - If the instance is composite → selects `composite_class_mutable` or `composite_class_immutable`.
    - The selection strategy is entirely driven by the metadata record of the target class (`cls.meta`).
    """

    if is_atom:
        return (
            cls.meta.atom_class_mutable
            if mutable else
            cls.meta.atom_class_immutable
        )
    else:
        return (
            cls.meta.composite_class_mutable
            if mutable else
            cls.meta.composite_class_immutable
        )


_DESIGN_NOTES = """
# get_base_class

## Purpose
Acts as the operational routing matrix dispatcher within the compilation ecosystem, selecting the pre-compiled structural class layout based on the object's classification and mutability state.

## Architectural Design Decisions

### 1. Matrix State Resolution Topology
* The router maps two independent, orthogonal state dimensions: Structural Topology (Atomic vs. Composite) and State Mutability (Mutable vs. Immutable).
* Using nested inline conditional blocks ensures quick, predictable branching at runtime, preventing complex, slow dictionary lookups or strategy pattern abstractions.

### 2. Encapsulated Metadata Delegation
* Instead of having the instance factory compile or store structural layouts directly, the function delegates this responsibility to `cls.meta`.
* This setup maintains clear boundaries: the instance factory coordinates object assembly, while the metadata layers handle class caching, layout compilation, and memory reuse strategies.

### 3. Leverage of Lazy Compilation Gateways
* The resolution pathways hook directly into the lazy evaluation properties (`atom_class_*` / `composite_class_*`) defined in the metadata layer.
* This deferred design pattern ensures that heavy dynamic class compilation workflows (like building internal properties, slot layouts, and tree structures) are executed only when a specific object configuration is actively created for the first time.
"""