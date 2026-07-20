from typing import TYPE_CHECKING
from collections.abc import Callable
# Inners
from ._get_inner_instance_class import _get_inner_instance_class
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance.core_classes import CompositeInstanceProtocol


def create_composite_init(
    meta: "SimpleMetadataLike",
    base_class_name: str,
    *,
    mutable: bool = True
) -> Callable:
    """Generates a universal initialization method closure for composite instances.

    Instantiates all immediate internal structural child nodes (inners) and establishes
    the core structural parent-child ownership link bindings across the composite graph.
    """

    def __init__(
        self: "CompositeInstanceProtocol"
    ) -> None:
        # 1. Invoke the constructor of the foundational ancestor (AtomBase)
        # This populates standard base slots like self._value and initializes the parent link
        if mutable:
            # noinspection PyArgumentList
            meta.atom_class_mutable.__init__(self)
        else:
            # noinspection PyArgumentList
            meta.atom_class_immutable.__init__(self)

        # 2. Iterate through all immediate children defined inside the component metadata schema
        for inner in meta.inners:
            inner_meta = inner.meta

            # Resolve the active compiled class descriptor for this specific sub-component
            # (routes dynamically to either the appropriate atom_class or composite_class)
            inner_instance_cls = _get_inner_instance_class(inner_meta, mutable)

            # Instantiate a clean instance of the internal child node (strictly parameterless)
            inner_instance = inner_instance_cls()

            # Establish structural binding: set this composite instance as the child's owner
            inner_instance._owner = self

            # Inject the instantiated child directly into its designated private layout slot
            setattr(self, inner_meta.name_private, inner_instance)

    # Re-bind dynamic reflection attributes to guarantee transparent stack traces and diagnostics
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    return __init__


_DESIGN_NOTES = """
# create_composite_init

## Purpose
Dynamically builds the initialization pipeline (`__init__`) for generated composite classes (`type(...)`). It coordinates structural tree allocations, ensuring that when a root or sub-tree composition node is born, its entire downstream nested object layout is generated and interlinked instantly.

## Architectural Design Decisions

### 1. Manual Ancestor MRO Triggering
* Instead of utilizing standard Python cooperative multiple inheritance through `super().__init__()`, this routine deliberately bypasses standard MRO path traversal. It directly addresses the explicit target initialization bindings via `meta.atom_class_mutable.__init__(self)`.
* This isolation prevents diamond-inheritance initialization collision bugs and eliminates the dynamic lookup overhead of `super()`, optimizing initialization loops across massive composition hierarchies.

### 2. Parameterless Cascading Tree Instantiation
* Child nodes are allocated via a clean `inner_instance_cls()` execution loop. This decouples object generation from external runtime argument signatures.
* Every component initializes cleanly into its natural structural state (using defaults pulled directly from its respective metadata context), allowing complex business object structures to allocate deterministically.

### 3. Backlink Inversion (`_owner = self`)
* Immediately upon allocation, the child instance receives a pointer linking back to its parent container via `inner_instance._owner = self`. 
* This bi-directional link allows mutations occurring inside leaf parameters to bubble up to container objects, executing reactive recalculation flows across the tree without requiring high-overhead global observer frameworks.

### 4. Direct Slot Allocation Safety
* The runtime values are bound to the instance using `setattr(self, inner_meta.name_private, inner_instance)`. 
* Since the parent class restricts its runtime footprint through explicit private variable tracking tokens in `__slots__`, this operation maps memory directly to fixed slot arrays, preserving high-performance operations and memory predictability.
"""