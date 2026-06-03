from typing import Iterator, Tuple, Any

from .Iter import IterMixin
from .Getitem import GetitemMixin

class ValuesMixin(IterMixin, GetitemMixin):
    """
    Vrací items, keys a values vnitřních prvků.
    """


    def values(self) -> Iterator[Any]:
        """Vrací instance všech vnitřních prvků."""
        for key in self:
            yield self[key]


__DOCT__ = """
**Purpose:**
`values()` returns a view of all values in the mapping.

**Signature:**
```python
def values(self):
    return self._data.values()
```
"""