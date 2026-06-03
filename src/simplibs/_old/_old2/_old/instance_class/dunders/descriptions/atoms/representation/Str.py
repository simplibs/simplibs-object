from typing import Any


class StrMixin:
    """
    Uživatelsky přívětivá reprezentace objektu (__str__).
    """
    __slots__ = ()
    value: Any

    def __str__(self) -> str:
        return str(self.value)


__DOCT__ = """
**Purpose:**
Defines the *human-readable* string representation of an object. This is what `print(obj)`,
`str(obj)`, and f-strings (`f"{obj}"`) use. It should be legible, concise, and aimed at
end users — not necessarily unambiguous or reconstructable. If `__str__` is not defined,
Python falls back to `__repr__`.

**Signature:**
```python
def __str__(self) -> str:
    return f"MyObject({self.value})"
```

**Called automatically when:**
```python
str(obj)        # explicit
print(obj)      # print() calls str() internally
f"{obj}"        # f-string uses __format__ which falls back to __str__
f"{obj!s}"      # explicit str conversion in f-string
```

**Relationships:**
- Falls back from `__format__` if no format spec is given.
- `__repr__` is the developer-facing twin — if only one is defined, define `__repr__`.
- `__bytes__` is the byte-string equivalent.

**Example:**
```python
class Product:
    def __init__(self, name, price): self.name, self.price = name, price
    def __str__(self): return f"{self.name}: ${self.price:.2f}"
    def __repr__(self): return f"Product({self.name!r}, {self.price!r})"

p = Product("Apple", 1.5)
print(p)          # Apple: $1.50   ← __str__
print(repr(p))    # Product('Apple', 1.5)   ← __repr__
```
"""