from typing import TYPE_CHECKING, Callable
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import CompositeInstanceProtocol


def create_recalculate_inners(
    meta: "SimpleMetadataLike",
    base_class_name: str,
) -> Callable:
    """Creates _recalculate_inners for composite instances."""

    def _recalculate_inners(self: "CompositeInstanceProtocol") -> None:
        # 1. Decompose composite value into per-inner shards
        decomposed = self.decompose_value(self._value)

        # 2. Push shards into child nodes
        for inner, inner_value in zip(meta.inners, decomposed):
            inner_instance = getattr(self, inner.meta.name_private)

            # 2.1 Write value without bubbling up
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(inner_value, recalculate_up=False)

            # 2.2 Cascade into nested composites
            if not inner.meta.is_constant:
                # noinspection PyProtectedMember
                inner_instance._recalculate_inners()

    _recalculate_inners.__name__ = "_recalculate_inners"
    _recalculate_inners.__qualname__ = f"{base_class_name}._recalculate_inners"
    _recalculate_inners.__annotations__ = {"return": None}

    return _recalculate_inners



_DESIGN_NOTES = """
# create_recalculate_inners

## Purpose
Synchronizes composite children when the parent’s value changes.  
Splits the parent value into shards and pushes them down the tree.

## Behavior
1. Calls `decompose_value` to obtain per-inner values.
2. For each inner:
   - writes the value using `_root_value_setter(..., recalculate_up=False)`
   - cascades into nested composites via `_recalculate_inners()`

## Notes
- `recalculate_up=False` prevents infinite parent-child update loops.
- Only composite children trigger recursive downward propagation.
- `zip(meta.inners, decomposed)` enforces strict positional alignment between
  declared inners and decomposed values.
"""