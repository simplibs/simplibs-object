from typing import TYPE_CHECKING
# Outers
from ...constants import BASE_CLASS_NAMES
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike


def calculate_blueprint_path(
    cls: "SimpleClassLike"
) -> str:
    """Builds a readable inheritance path for the class."""

    # 1. Local import to avoid circular dependencies
    from .....SimpleBase import SimpleBase

    # 2. Collect relevant parents from MRO
    parents = [
        base.__name__
        for base in cls.__mro__
        if issubclass(base, SimpleBase)
        and base.__name__ not in BASE_CLASS_NAMES
        and base is not cls
    ]

    # 3. Construct path
    return (
        cls.__name__
        if not parents else
        f"{cls.__name__}({', '.join(parents)})"
    )



_DESIGN_NOTES = """
# calculate_blueprint_path

## Purpose
Creates a readable inheritance path for a Simple class.  
Used mainly in `__repr__` to show the blueprint structure of a class without
framework noise.

## How it works
The function inspects the class MRO and selects only meaningful ancestors:

1. **SimpleBase filter**  
   Only classes that inherit from `SimpleBase` are considered part of the
   SimpleObject ecosystem.

2. **Framework root exclusion**  
   Classes listed in `BASE_CLASS_NAMES` (e.g., `SimpleBase`, `SimpleConstant`,
   `SimpleObject`) are skipped. They are structural roots, not business-level
   ancestors.

3. **Self exclusion**  
   The class itself is not included in the parent list.

## Output format
- **No custom parents**  
  Returns only the class name:  
  `"MyClass"`

- **With custom parents**  
  Returns a bracketed list:  
  `"MyClass(ParentA, ParentB)"`

The order follows the class MRO.

## Examples

| Class hierarchy                         | Output                         |
|-----------------------------------------|--------------------------------|
| `MyConstant(SimpleConstant)`            | `"MyConstant"`                 |
| `MyObject(BaseObject, SimpleObject)`    | `"MyObject(BaseObject)"`       |
| `Child(ParentA, ParentB, SimpleObject)` | `"Child(ParentA, ParentB)"`    |

## Notes
- The internal import of `SimpleBase` prevents circular imports during early
  metadata initialization.
- Complexity is O(m), where m is the MRO depth (typically very small).
"""
