from typing import TYPE_CHECKING, Callable
# Inners
from ._get_inner_instance_class import _get_inner_instance_class
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import CompositeInstanceProtocol


def create_composite_init(
    meta: "SimpleMetadataLike",
    base_class_name: str,
    *,
    mutable: bool = True,
) -> Callable:
    """Creates __init__ for composite instances."""

    def __init__(self: "CompositeInstanceProtocol") -> None:
        # 1. Instantiate and bind all immediate inner nodes
        for inner in meta.inners:
            inner_meta = inner.meta
            inner_cls = _get_inner_instance_class(inner_meta, mutable)
            inner_instance = object.__new__(inner_cls)
            inner_instance.__init__()
            inner_instance._owner = self
            setattr(self, inner_meta.name_private, inner_instance)

        # 2. Initialize base atom class (triggers combined init_mixins)
        if mutable:
            # noinspection PyArgumentList
            meta.atom_class_mutable.__init__(self)
        else:
            # noinspection PyArgumentList
            meta.atom_class_immutable.__init__(self)

    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    return __init__


_DESIGN_NOTES = """
# create_composite_init

## Purpose
Builds the `__init__` method for composite instance classes.  
Allocates and attaches all inner child nodes prior to running atom initialization and mixin lifecycles.

## Behavior
1. Iterates over `meta.inners` and:
   - resolves the correct instance class via `_get_inner_instance_class`
   - allocates raw memory via `object.__new__(inner_cls)` to bypass `SimpleMeta.__call__`
   - executes `inner_instance.__init__()` to apply initialization logic recursively
   - assigns `_owner` to establish parent linkage
   - stores the instance into its designated private slot
2. Calls the correct atom-class initializer (`meta.atom_class_mutable` or `meta.atom_class_immutable`),
   which executes `_build_combined_init_mixins` pipeline across all registered mixins.

## Ordering Invariant
Inner nodes MUST be instantiated and attached before calling the atom class `__init__`.
Mixins initialized during the atom phase (such as `NodesTuple` and `NodesDicts`) inspect
the composite structure and require immediate access to all child slots (e.g. `_pair`).
Instantiating children first ensures the object tree is complete before structural mixins run.

## Notes
- Avoids `super()` to prevent MRO complexity and ensure deterministic initialization.
- Uses direct memory allocation (`object.__new__`) followed by `__init__()` for inner nodes. 
  This explicitly bypasses `SimpleMeta.__call__`, preventing the metaclass from treating 
  an already generated runtime class as a new declarative blueprint.
- All inner nodes are created parameterlessly, relying on metadata defaults.
- `_owner` establishes the bidirectional link required for reactive recalculation.
- Does not call `self.init_mixins()` directly; mixin initialization is strictly delegated to the atom base.
"""