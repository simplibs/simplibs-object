# numeric/inplace/Iadd.py
class IaddMixin:
    __slots__ = ()
    value: Any

    def __iadd__(self, other):
        try:
            other_value = getattr(other, "value", other)
            self.value = self.value + other_value
            return self
        except TypeError:
            return NotImplemented

__DOCT__ = """
**Purpose:**
Implements `+=`. Should mutate `self` in-place and return `self`. If it is not defined,
Python falls back to `__add__` and creates a new object.

**Signature:**
```python
def __iadd__(self, other):
    self.value += other.value   # mutate
    return self                 # MUST return self
```

**Called automatically when:**
```python
a += b   # calls a.__iadd__(b); result is reassigned to a
```

**Relationships:**
- Fallback: `__add__` (Python creates a new object).
- All in-place variants follow this same pattern: mutate + return self.

**Example:**
```python
class Counter:
    def __init__(self, n): self.n = n
    def __iadd__(self, other):
        self.n += other if isinstance(other, int) else other.n
        return self
    def __repr__(self): return f"Counter({self.n})"

c = Counter(5)
c += 3
print(c)  # Counter(8) — same object mutated
```
"""