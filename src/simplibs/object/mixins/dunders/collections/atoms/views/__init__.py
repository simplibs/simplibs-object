from .Items import ItemsMixin
from .Keys import KeysMixin
from .Values import ValuesMixin

__all__ = (
    "ItemsMixin",
    "KeysMixin",
    "ValuesMixin",
)


__DOCT__ = """
## `collections/keys/`

> **Subgroup purpose:**
> The keys/values/items trio provides dict-like view interfaces. These are not dunder
> methods in the strict sense (they do not have `__double_underscore__` form), but they
> are part of the standard Mapping protocols that Python's `collections.abc.Mapping`
> expects. Defining them makes your class compatible with code that treats it as a mapping.
"""