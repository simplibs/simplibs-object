# numeric/inplace/Imod.py
class ImodMixin:
    __slots__ = ()
    value: Any

    def __imod__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value % other_value
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

__DOCT__ = """
**Purpose:** Implements `%=`.

**Signature:**
```python
def __imod__(self, other):
    self.value %= other
    return self
```

**Called automatically when:** `a %= b`
"""