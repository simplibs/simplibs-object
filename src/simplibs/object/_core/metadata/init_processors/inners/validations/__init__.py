from .validate_inner_is_class import validate_inner_is_class
from .validate_inner_is_not_simple_class import validate_inner_is_not_simple_class
from .validate_inner_is_simple_subclass import validate_inner_is_simple_subclass

from .validate_inners_is_defined import validate_inners_is_defined
from .validate_inners_is_not_empty import validate_inners_is_not_empty
from .validate_inners_is_tuple import validate_inners_is_tuple

from .validate_collision_within_inners import validate_collision_within_inners
from .validate_if_collision_with_owner_class import validate_if_collision_with_owner_class


_DESIGN_NOTES = """
# Inners Validation Sub-Package

## Purpose
Provides all validation filters applied to `_inners` and its elements. Ensures
structural correctness, type lineage, and identifier uniqueness across the
composition tree.

## Internal Components Registry

| Component                                | Type     | Description                                                                |
| :--------------------------------------- | :------- | :------------------------------------------------------------------------- |
| `validate_inner_is_class`                | Function | Ensures each inner element is a class object.                              |
| `validate_inner_is_not_simple_class`     | Function | Blocks using raw Simple framework base classes.                            |
| `validate_inner_is_simple_subclass`      | Function | Verifies inheritance from Simple base classes.                             |
| `validate_inners_is_defined`             | Function | Checks that `_inners` is present on the class.                             |
| `validate_inners_is_not_empty`           | Function | Rejects empty `_inners` declarations.                                      |
| `validate_inners_is_tuple`               | Function | Ensures `_inners` is a tuple.                                              |
| `validate_collision_within_inners`       | Function | Detects name collisions among sibling inner elements.                      |
| `validate_if_collision_with_owner_class` | Function | Prevents inner elements from sharing the owner's identifier.               |
"""
