from typing import Iterator, Tuple, Any

from .Iter import IterMixin
from .Getitem import GetitemMixin

class KeysMixin(IterMixin, GetitemMixin):
    """
    Vrací items, keys a values vnitřních prvků.
    """

    def keys(self) -> Iterator[str]:
        """Vrací jména všech vnitřních prvků."""
        return self.__iter__()



__DOCT__ = """
**Purpose:**
`keys()` returns a view (or iterable) of all keys in the mapping. Part of the Mapping
ABC interface. The standard implementation returns a `KeysView` from `collections.abc`,
which provides set-like operations on keys.

**Signature:**
```python
def keys(self):
    return self._data.keys()   # or iter(self._data)
```

**Called automatically when:**
```python
for k in mapping.keys(): ...
mapping.keys() & other_keys   # set operations on keys
```

**Relationships:**
- Sibling of `values()` and `items()`.
- Required by `collections.abc.Mapping`.
- `__iter__` typically iterates keys for mapping types (mirrors `keys()`).
"""