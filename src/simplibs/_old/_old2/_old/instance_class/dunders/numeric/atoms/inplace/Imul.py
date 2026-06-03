# numeric/inplace/Imul.py
class ImulMixin:
    __slots__ = ()
    value: Any

    def __imul__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value * other_value
            return self
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:** Implements `*=`.

**Signature:**
```python
def __imul__(self, other):
    self.value *= other
    return self
```

**Called automatically when:** `a *= b`
"""