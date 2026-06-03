from typing import Iterator


class ReversedMixin:
    __slots__ = ()

    def __reversed__(self) -> Iterator:
        if hasattr(self, "meta") and hasattr(self.meta, "inners"):
            return reversed([inner.name_snake for inner in self.meta.inners])
        return iter([])


__DOCT__ = """
**Purpose:**
Defines `reversed(obj)`. If not defined, `reversed()` requires `__len__` and `__getitem__`
(sequence protocol) and constructs a reverse iterator automatically. Define `__reversed__`
when you can provide a more efficient reverse iteration than scanning backwards through indices.

**Signature:**
```python
def __reversed__(self):
    return iter(reversed(self._data))
```

**Called automatically when:**
```python
reversed(obj)         # returns an iterator
list(reversed(obj))   # common use
```

**Relationships:**
- If absent, Python falls back to `__len__` + `__getitem__` (sequence fallback).
- Works with `__iter__` — they are independent but often both defined.
"""