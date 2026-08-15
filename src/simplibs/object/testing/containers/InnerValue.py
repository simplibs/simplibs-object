from dataclasses import dataclass
from typing import Any, Iterable
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ._validations import (
    raise_inner_value_empty_path,
    raise_inner_value_invalid_path_type,
)


@dataclass(frozen=True)
class InnerValue:
    """Represents a target property path update and value payload for nested composite testing.

    Encapsulates nested property paths (e.g. ``"address.city.zip"`` or ``("address", "city", "zip")``)
    and their corresponding target test values. Normalizes path specifications into uniform string tuples
    and provides dynamic instance navigation utilities.

    Args:
        path: A dot-separated property path string or an iterable sequence of string attribute identifiers.
        value: Candidate payload value to assign or assert at the resolved property location.
    """

    path: str | Iterable[str]
    value: Any

    def __post_init__(self) -> None:
        """Normalizes and validates the property path upon dataclass initialization.

        Raises:
            SimpleLogicError: If the path evaluates to an empty sequence or contains non-string items.
        """
        # 1. Normalize path input into a list of string segments
        if isinstance(self.path, str):
            parts = self.path.split(".")
        else:
            parts = tuple(self.path)

        # 2. Validate non-empty path constraint
        if not parts:
            raise_inner_value_empty_path()

        # 3. Validate string item types in path
        for part in parts:
            if not isinstance(part, str):
                raise_inner_value_invalid_path_type(self.path, part)

        # 4. Freeze normalized path as an immutable tuple of strings
        object.__setattr__(self, "path", tuple(parts))

    def as_instance_tuple(self, instance: Any) -> tuple[Any, Any] | UnsetType:
        """Navigates nested child instances and returns the target parent instance and value pair.

        Traverses child composite property chains using the convention ``<part>_instance``. If any intermediate
        property is missing or resolves to ``None``, returns ``UNSET``.

        Args:
            instance: Root composite object instance to traverse.

        Returns:
            A tuple ``(resolved_inner_instance, target_value)`` if navigation succeeds, otherwise ``UNSET``.
        """
        current = instance

        for part in self.path:
            inner_prop = f"{part}_instance"

            if not hasattr(current, inner_prop):
                return UNSET

            current = getattr(current, inner_prop)

            if current is None:
                return UNSET

        return current, self.value


_DESIGN_NOTES = """
# InnerValue (Nested Property Mutation & Assert Value Container)

## Purpose
Acts as a declarative value-and-path container used during upward/downward reactivity testing, 
state mutation assertions, and parameter tests on nested `SimpleObject` composites.

## Path Normalization & Exception Safeguards
1. **Normalization:** Converted from dot-notation strings (`"address.city"`) or sequences (`("address", "city")`) 
   into an immutable tuple of string segments (`("address", "city")`).
2. **Validation Errors:**
   - Empty path -> Triggers `raise_inner_value_empty_path()` (`SimpleLogicError` wrapping `ValueError`).
   - Non-string path segments -> Triggers `raise_inner_value_invalid_path_type()` (`SimpleLogicError` wrapping `TypeError`).

## Navigation Lifecycle (`as_instance_tuple`)
Navigates composite hierarchies via `getattr(current, f"{part}_instance")`. 
If all nested instances exist, returns `(target_inner_instance, target_value)`. 
If any intermediate reference is missing or `None`, gracefully returns `UNSET`.

## Framework Usage Locations
1. **`asserts/reactivity/assert_reactivity_upward.py`:** Reads `.as_instance_tuple(instance)` to perform child property mutation and root recalculation checks.
2. **`asserts/base/assert_value_change.py`:** Detects `isinstance(value, InnerValue)` to unpack targeted nested value updates.
3. **`assert_simple_object.py`:** Used in parameter signatures (`test_value_change`, `test_reactivity_up`, `test_mutability`, `test_immutability`).
"""