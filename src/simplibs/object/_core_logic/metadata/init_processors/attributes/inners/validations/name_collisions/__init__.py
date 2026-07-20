from .validate_collision_within_inners import validate_collision_within_inners
from .validate_if_collision_with_owner_class import validate_if_collision_with_owner_class


_DESIGN_NOTES = """
# Name Collisions Validation Sub-Package

## Purpose
Houses deep tree-traversal identifier validation filters that safeguard the global composite namespace from duplicate assignments.

## Internal Components Registry

| Component                                | Type     | Description                                                                          |
| :--------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_collision_within_inners`       | Function | Scans siblings down the composition branch to isolate and pinpoint identifier clashes.|
| `validate_if_collision_with_owner_class` | Function | Blocks child elements from matching the parent class identity to avoid recursion loops.|
"""