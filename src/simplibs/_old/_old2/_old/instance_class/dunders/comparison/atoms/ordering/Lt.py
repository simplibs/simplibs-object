class LtMixin:
    def __lt__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value < other_value
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:**
Defines `<` (less than). The most fundamental ordering relation — `functools.total_ordering`
can derive `__le__`, `__gt__`, `__ge__` from just `__eq__` + `__lt__`.
Return `NotImplemented` for unsupported types.

**Signature:**
```python
def __lt__(self, other) -> bool:
    if not isinstance(other, type(self)):
        return NotImplemented
    return self.value < other.value
```

**Called automatically when:**
```python
a < b
sorted([a, b, c])   # sorting uses __lt__
min(a, b, c)        # also uses __lt__
```

**Relationships:**
- With `__eq__`, sufficient for `functools.total_ordering`.
- `__gt__` is the reflected version: `a < b` ↔ `b > a`.
- Used by `sorted()`, `min()`, `max()`, `heapq`.
"""