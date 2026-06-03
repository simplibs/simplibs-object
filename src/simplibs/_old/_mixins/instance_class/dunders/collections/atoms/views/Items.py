from typing import Iterator, Tuple, Any

from .Iter import IterMixin
from .Getitem import GetitemMixin

class ItemsMixin(IterMixin, GetitemMixin):
    """
    Vrací items, keys a values vnitřních prvků.
    """

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Vrací dvojice (jméno, instance)."""
        for key in self:
            yield key, self[key]


__DOCT__ = """
**Purpose:**
`items()` returns a view of `(key, value)` pairs. This is what `for k, v in mapping.items()`
uses, and what dict unpacking relies on.

**Signature:**
```python
def items(self):
    return self._data.items()
```
"""