from typing import TYPE_CHECKING
# Outers
from ....properties import create_value_property
# Inners
from .helpers import (
    create_composite_init,
    create_recalculate_self,
    create_recalculate_inners,
    create_properties_for_inners
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import CompositeInstanceProtocol


def make_composite_class(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True
) -> "CompositeInstanceProtocol":
    """Main orchestrator compiling a structural composite instance class (Node).

    Synthesizes either a mutable or an immutable structural variant at runtime based on
    the explicitly supplied `mutable` configuration matrix constraint.
    """

    # 1. Resolve and establish the compiled class string identification nomenclature
    base_class_name = (
        f"{meta.class_name}CompositeMutableBase"
        if mutable else
        f"{meta.class_name}CompositeImmutableBase"
    )

    # 2. Extract and establish the proper ancestor inheritance chain (MRO target)
    base_class = meta.atom_class_mutable if mutable else meta.atom_class_immutable
    class_parents = (base_class,)

    # 3. Assemble the core class namespace dictionary definition payload
    class_dict = {
        "__doc__": f"Composite structural instance object tracking {meta.class_name}",
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name, mutable=mutable),
        "value": create_value_property(meta, is_constant=False, mutable=mutable),
    }

    # 4. Merge descriptor property blueprints for immediate children into the namespace
    class_dict |= create_properties_for_inners(meta, mutable=mutable)

    # 5. Inject reactive recalculation hooks exclusively into the mutable namespace variant
    if mutable:
        class_dict["_recalculate_self"] = create_recalculate_self(meta, base_class_name)
        class_dict["_recalculate_inners"] = create_recalculate_inners(meta, base_class_name)

    # 6. Materialize the type blueprint into a concrete live class structure
    # noinspection PyTypeChecker
    composite_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 7. Clean up internal declarative schema vectors from the runtime class space
    for name in ("inners", "_logic", "_decompose"):
        if name in composite_class.__dict__:
            delattr(composite_class, name)

    # 8. Return the fully compiled type object matching the protocol interface
    composite_class: "CompositeInstanceProtocol"
    return composite_class


_DESIGN_NOTES = """
# make_composite_class

## Purpose
Acts as the central factory engine responsible for the dynamic compilation of composite types (`type(...)`). It transforms raw structural schema metadata arrays into optimized class structures, creating high-performance instances that orchestrate tree state relationships.

## Architectural Design Decisions

### 1. Dynamic Type Metaprogramming Synthesis (`type(...)`)
* By invoking Python's native `type(name, bases, dict)` constructor, this function handles type generation entirely at runtime. It avoids code-generation strings or unsafe `exec` blocks.
* This dynamic compilation compiles the entire descriptor map, slot layout, and initialization pipelines directly into the Python C-level structure at application boot or schema loading time. The approach guarantees that subsequent runtime instance allocations run at native C-extension speeds.

### 2. Micro-Optimized Memory Layouts via Slot Chaining
* The generator calculates `__slots__` explicitly using the private structural nomenclature tokens (`inner.meta.name_private`).
* Because `class_parents` references the compiled `atom_class` (which also defines `__slots__`), this creates a strict slot inheritance chain. 
* As a result, every instance allocated from this compiled class lacks a local `__dict__`, packing memory into predictable pointers. This enables fast access times and keeps memory footprints compact when dealing with trees containing millions of nodes.

### 3. Namespace Asymmetry Matrix
* The injection of `_recalculate_self` and `_recalculate_inners` is explicitly restricted to the `mutable` path execution branch (`if mutable:`).
* Immutable nodes do not require data propagation mechanics since their states cannot drift post-initialization. Excluding these methods keeps the internal namespace clean and helps prevent invalid state changes from occurring on read-only structures.

### 4. Interface Cleanup and Attribute Leaking Protection
* In step 7, the function cleans up the class namespace using `delattr` to remove declarative tokens (`inners`, `_logic`, `_decompose`).
* This step ensures that raw metadata definition vectors are scrubbed from the compiled runtime type namespace. Users and automated serialization tools are protected from accessing raw layout blueprints when inspecting live structural object instances.
"""