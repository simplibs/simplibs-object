# numeric/inplace/Isub.py
class IsubMixin:
    __slots__ = ()
    value: Any

    def __isub__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value - other_value
            return self
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:** Implements `-=`. Mutate in-place and return `self`.

**Signature:**
```python
def __isub__(self, other):
    self.value -= other
    return self
```

**Called automatically when:** `a -= b`
"""