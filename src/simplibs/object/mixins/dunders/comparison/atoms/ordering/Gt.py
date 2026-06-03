class GtMixin:
    def __gt__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value > other_value
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:**
Defines `>` (greater than). Note: Python does NOT automatically derive `__gt__` from
`__lt__` — you must define it (or use `total_ordering`). `a > b` first calls `a.__gt__(b)`;
if `NotImplemented`, then `b.__lt__(a)`.

**Signature:**
```python
def __gt__(self, other) -> bool:
    if not isinstance(other, type(self)): return NotImplemented
    return self.value > other.value
```

**Called automatically when:** `a > b`
"""