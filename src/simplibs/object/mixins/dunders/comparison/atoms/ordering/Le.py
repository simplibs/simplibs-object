class LeMixin:
    # Varianta 1: Využít Lt + Eq (vyžaduje oba mixiny)
    def __le__(self, other):
        return self == other or self < other

    # Varianta 2: Samostatná logika
    def __le__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value <= other_value
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:** Defines `<=` (less than or equal to).

**Signature:**
```python
def __le__(self, other) -> bool:
    if not isinstance(other, type(self)): return NotImplemented
    return self.value <= other.value
```

**Called automatically when:** `a <= b`
"""