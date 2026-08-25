from typing import TYPE_CHECKING
# Outers
from ....logic.property_builders import create_value_property
# Inners
from .helpers import (
    create_composite_init,
    create_recalculate_self,
    create_recalculate_inners,
    create_properties_for_inners,
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.instance.core_classes import CompositeInstanceProtocol


def make_composite_class(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True,
) -> "CompositeInstanceProtocol":
    """Builds a composite instance class for the given metadata."""

    # 1. Class name
    base_class_name = (
        f"{meta.class_name}CompositeMutableBase"
        if mutable
        else f"{meta.class_name}CompositeImmutableBase"
    )

    # 2. Base class / MRO
    base_class = meta.atom_class_mutable if mutable else meta.atom_class_immutable
    class_parents = (base_class,)

    # 3. Core namespace
    class_dict = {
        "__metadata__": meta,
        "__doc__": f"Composite structural instance object tracking {meta.class_name}",
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name, mutable=mutable),
        "value": create_value_property(meta, is_constant=False, mutable=mutable),
    }

    # 4. Properties for inners
    class_dict |= create_properties_for_inners(meta, mutable=mutable)

    # 5. Reactive hooks (mutable only)
    if mutable:
        class_dict["_recalculate_self"] = create_recalculate_self(meta, base_class_name)
        class_dict["_recalculate_inners"] = create_recalculate_inners(meta, base_class_name)

    # 6. Materialize type
    # noinspection PyTypeChecker
    composite_class = type(base_class_name, class_parents, class_dict)

    composite_class: "CompositeInstanceProtocol"
    return composite_class


_DESIGN_NOTES = """
# make_composite_class

## Purpose
Compiles a concrete composite instance class from metadata.  
Builds the runtime type that represents a composition node, with slots, properties,
initialization, and reactive hooks.

## Behavior
1. Derives a unique class name for mutable/immutable variants.
2. Chooses the correct atom base class and sets it as the sole parent (inheriting `_is_instance_class` from `InstanceBase`).
3. Builds the class namespace:
   - `__metadata__ = meta` to preserve declarative blueprint metadata on the class
   - `__slots__` from `inner.meta.name_private`
   - `__init__` from `create_composite_init`
   - `value` from `create_value_property`
4. Merges properties for all immediate inners via `create_properties_for_inners`.
5. For mutable variants, injects `_recalculate_self` and `_recalculate_inners`.
6. Creates the type using `type(name, bases, dict)`.

## Notes
- Using `type(...)` keeps compilation safe and explicit, without `exec`.
- Inherited `_is_instance_class` and assigned `__metadata__` prevent `SimpleMeta` from treating 
  dynamically created composite types as new declarative classes.
- Explicit `__slots__` and atom base inheritance produce a compact, predictable
  memory layout without per-instance `__dict__`.
- Reactive hooks exist only on mutable composites; immutable ones are structurally
  frozen after initialization.
- `class_dict` passed to `type(...)` only ever contains the members listed above — declarative
  attributes such as `inners`, `_logic`, and `_decompose` are never placed there, so they are
  never present on the compiled class's own `__dict__` in the first place. They remain reachable
  through the MRO via the atom base class / `meta.owner_class`, since `type(...)` only controls
  the new class's own namespace, not what its parents already expose.
"""
