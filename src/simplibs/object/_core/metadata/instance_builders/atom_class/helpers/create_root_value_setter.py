from typing import Any, TYPE_CHECKING, Callable
# Annotations
if TYPE_CHECKING:
    from .....protocols.instance import SimpleInstanceLike


def create_root_value_setter(
    base_class_name: str,
) -> Callable:
    """Creates the _root_value_setter method for mutable atomic instances."""

    # 1. Setter closure
    def _root_value_setter(
        self: "SimpleInstanceLike",
        value: Any,
        recalculate_up: bool = True,
    ) -> None:

        # 1. Normalize incoming value
        new_value = self.normalize(value, process_none=True)

        # 2. Short-circuit if unchanged
        if self._value == new_value:
            return

        # 3. Assign new value
        self._value = new_value

        # 4. Trigger owner recalculation
        if self._owner and recalculate_up:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # 2. Reflection alignment
    _root_value_setter.__name__ = "_root_value_setter"
    _root_value_setter.__qualname__ = f"{base_class_name}._root_value_setter"
    _root_value_setter.__annotations__ = {
        "value": Any,
        "recalculate_up": bool,
        "return": None,
    }

    # 3. Return setter
    return _root_value_setter



_DESIGN_NOTES = """
# create_root_value_setter

## Purpose
Generates the `_root_value_setter` method used by mutable atomic instances.
This setter is responsible for:
- normalization,
- value assignment,
- and triggering reactive recalculation on the owner.

## Behavior
1. Normalizes the incoming value using the instance’s `normalize` method.
2. Performs a fast equality check to avoid unnecessary recalculation.
3. Assigns the new value.
4. If the instance has an owner and bubbling is enabled, triggers `_recalculate_self`.

## Notes
This function is internal to the instance-building pipeline and is not part of
the public API. It is intentionally minimal and optimized for performance.
"""