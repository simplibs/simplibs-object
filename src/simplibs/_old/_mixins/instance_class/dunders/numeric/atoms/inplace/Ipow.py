# numeric/inplace/Ipow.py
class IpowMixin:
    __slots__ = ()
    value: Any

    def __ipow__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value ** other_value
            return self
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:** Implements `**=`.

**Signature:**
```python
def __ipow__(self, other):
    self.value **= other
    return self
```

**Called automatically when:** `a **= b`
"""