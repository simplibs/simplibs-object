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
        # 1. Initialize base atom class
        if mutable:
            # noinspection PyArgumentList
            meta.atom_class_mutable.__init__(self)
        else:
            # noinspection PyArgumentList
            meta.atom_class_immutable.__init__(self)

        # 2. Instantiate all immediate inner nodes
        for inner in meta.inners:
            inner_meta = inner.meta
            inner_cls = _get_inner_instance_class(inner_meta, mutable)
            inner_instance = inner_cls()
            inner_instance._owner = self
            setattr(self, inner_meta.name_private, inner_instance)

        # 3. Trigger mixin initialization
        self.init_mixins()

    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    return __init__



_DESIGN_NOTES = """
# create_composite_init

## Purpose
Builds the `__init__` method for composite instance classes.  
Allocates all inner nodes, links them to their parent, and initializes the base atom class.

## Behavior
1. Calls the correct atom-class initializer (mutable or immutable).
2. Iterates over `meta.inners` and:
   - resolves the correct instance class via `_get_inner_instance_class`
   - instantiates the inner node
   - assigns `_owner`
   - stores the instance into its private slot
3. Calls `init_mixins()` to allow mixins to attach initialization logic.

## Notes
- Avoids `super()` to prevent MRO complexity and ensure deterministic initialization.
- All inner nodes are created parameterlessly, relying on metadata defaults.
- `_owner` establishes the bidirectional link required for reactive recalculation.
- Slot assignment is safe and fast due to fixed `__slots__` layout.
"""