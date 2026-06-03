class GeMixin:
    def __ge__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value >= other_value
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:** Defines `>=` (greater than or equal to).

**Signature:**
```python
def __ge__(self, other) -> bool:
    if not isinstance(other, type(self)): return NotImplemented
    return self.value >= other.value
```

**Called automatically when:** `a >= b`

---

*— End of Part 1 —*
*Continue in Part 2: Representation · Collections · Iteration · Context · Callable · Async · AAA*
"""