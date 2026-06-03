# numeric/inplace/Ifloordiv.py
class IfloordivMixin:
    __slots__ = ()
    value: Any

    def __ifloordiv__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value // other_value
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

__DOCT__ = """
**Purpose:** Implements `//=` (floor division in-place).

**Signature:**
```python
def __ifloordiv__(self, other):
    self.value //= other
    return self
```

**Called automatically when:** `a //= b`
"""