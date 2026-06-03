# numeric/inplace/Idiv.py
class IdivMixin:
    __slots__ = ()
    value: Any

    def __itruediv__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value / other_value
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

__DOCT__ = """
**Purpose:** Implements `/=` (true division in-place).

**Signature:**
```python
def __itruediv__(self, other):
    self.value /= other
    return self
```

**Called automatically when:** `a /= b`
"""