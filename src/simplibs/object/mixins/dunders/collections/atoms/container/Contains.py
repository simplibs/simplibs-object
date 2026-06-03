from typing import Any


class ContainsMixin:
    __slots__ = ()

    def __contains__(self, key: Any) -> bool:
        if hasattr(self, "meta") and hasattr(self.meta, "inners"):
            return any(inner.name_snake == key for inner in self.meta.inners)
        return False



__DOCT__ = """
**Purpose:**
Defines the `in` membership test operator. If `__contains__` is not defined, Python
falls back to iterating with `__iter__` (O(n)). A custom `__contains__` can provide
O(1) lookup for hash-based containers or O(log n) for sorted ones.

**Signature:**
```python
def __contains__(self, item) -> bool:
    return item in self._data
```

**Called automatically when:**
```python
item in obj       # calls obj.__contains__(item)
item not in obj   # calls not obj.__contains__(item)
```

**Relationships:**
- Fallback: if absent, Python iterates via `__iter__` to check membership.
- Commonly paired with `__getitem__` and `__len__` in container classes.

**Example:**
```python
class WordSet:
    def __init__(self, words): self._words = set(w.lower() for w in words)
    def __contains__(self, word): return word.lower() in self._words

ws = WordSet(["Hello", "World"])
print("hello" in ws)    # True — case-insensitive
print("Python" in ws)   # False
```
"""