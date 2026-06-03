from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class PosMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __pos__(self):
        try:
            return self.create_modified_instance(value=+self.value)
        except TypeError:
            return NotImplemented


__DOCT__ = """
**Purpose:**
Implements unary `+x`. For numbers this is almost always a no-op (returns a copy of
`self`), but it can be overloaded for custom semantics — e.g., `+Decimal` rounds to
the current context precision, `+Counter` removes zero and negative counts.

**Signature:**
```python
def __pos__(self):
    return type(self)(self.value)   # typically a copy
```

**Called automatically when:**
```python
+obj   # calls obj.__pos__()
```

**Relationships:** Complementary to `__neg__`.

"""