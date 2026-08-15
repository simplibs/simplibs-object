from typing import TYPE_CHECKING, Callable
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import CompositeInstanceProtocol


def create_recalculate_self(
    meta: "SimpleMetadataLike",
    base_class_name: str,
) -> Callable:
    """Creates _recalculate_self for composite instances."""

    def _recalculate_self(self: "CompositeInstanceProtocol") -> None:
        # 1. Collect current child values
        current_values = {
            inner.meta.name_snake: getattr(self, inner.meta.name_private).value
            for inner in meta.inners
        }

        # 2. Compute new composite value
        new_value = self.calculate_value(**current_values)

        # 3. Short-circuit if unchanged
        # noinspection PyBroadException
        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        # 4. Update local state
        self._value = new_value

        # 5. Bubble upward
        if self._owner:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    _recalculate_self.__name__ = "_recalculate_self"
    _recalculate_self.__qualname__ = f"{base_class_name}._recalculate_self"
    _recalculate_self.__annotations__ = {"return": None}

    return _recalculate_self



_DESIGN_NOTES = """
# create_recalculate_self

## Purpose
Aggregates child values, computes the composite’s new state, and propagates changes
upward through the composition tree.

## Behavior
1. Builds a `{name_snake: value}` map from all immediate children.
2. Calls `calculate_value(**current_values)` to compute the composite state.
3. If the value did not change, stops early to avoid unnecessary bubbling.
4. Updates `_value`.
5. If the composite has a parent, calls `_owner._recalculate_self()`.

## Notes
- The dictionary comprehension provides a clean boundary between structural layout
  and user-defined business logic.
- The equality check prevents redundant recalculation waves.
- The `try/except` guard ensures comparison errors do not break the reactive chain.
- This function forms the upward half of the reactive system; the downward half is
  implemented in `create_recalculate_inners`.
"""