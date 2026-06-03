from .collections import *
from .comparison import *
from .descriptions import *
from .lifecycle import *
from .numeric import *
from .protocols import *

__all__ = (
    *collections.__all__,
    *comparison.__all__,
    *descriptions.__all__,
    *lifecycle.__all__,
    *numeric.__all__,
    *protocols.__all__,
)


__DOCT__ = """
# Python Dunder Methods — Complete Reference

> **How to use this document:**
> Each entry follows the structure:
> - **Path** — where this atom lives in your project
> - **Purpose** — why this method exists, what problem it solves
> - **Signature** — the method signature as Python expects it
> - **Called automatically when** — what Python statement/operation triggers it
> - **Relationships** — how it connects to other dunders
> - **Example** — a minimal, complete code snippet


# APPENDIX: Dunders NOT in the atom structure (auto-managed or derived)

The following dunders exist in Python but are deliberately absent from your atom files
because they are either auto-managed, always derived from another dunder, or so
infrastructure-level that defining them manually would almost always be wrong.

| Dunder | Why it is excluded |
|---|---|
| `__class__` | Auto attribute — points to the type of the instance |
| `__doc__` | Auto attribute — the docstring. You use `__DOCT__` instead |
| `__module__` | Auto attribute — the module name |
| `__qualname__` | Auto attribute — qualified name (for nested classes) |
| `__name__` | Auto attribute on classes/functions |
| `__ne__` | Auto-derived from `__eq__` in Python 3 (define `Eq`, get `Ne` free) |
| `__radd__`, `__rsub__`, ... | Reflected variants — optional additions to arithmetic atoms, not separate atoms |
| `__iand__`, `__ior__`, ... | In-place bitwise — optional additions to bitwise atoms |
| `__index__` | Special integer protocols — semantically stronger than `__int__`; add to Int atom |
| `__trunc__` | Called by `math.trunc()` and fallback for `int()`; add to Int atom |
| `__length_hint__` | Optimization hint for `__length_hint__()` — rarely needed |
| `__init_subclass__` cls kwarg | The kwargs form — same atom, different usage |
| `__prepare__` | Metaclass-only — creates the class namespace dict |
| `__instancecheck__` | On metaclass — customizes `isinstance()` |
| `__subclasscheck__` | On metaclass — customizes `issubclass()` |
| `__set_name__` (on instance) | Already in `lifecycle/class_hooks/` |
| `__class_cell__` | Internal CPython implementation detail for `super()` |
| `__builtins__` | Module-level auto attribute |
| `__spec__`, `__loader__`, `__package__` | Module import system internals |
"""