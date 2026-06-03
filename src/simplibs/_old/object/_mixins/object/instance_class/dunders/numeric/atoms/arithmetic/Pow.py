from typing import Any
from .....methods.modificators import ModifyInstance


class PowMixin(ModifyInstance):
    __slots__ = ()

    # Očekává
    value: Any

    def __pow__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = self.value ** other_value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented

    def __rpow__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = other_value ** self.value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented


__DOCT__ = """
**Purpose:**
Implements the `**` exponentiation operator and the built-in `pow(base, exp, mod)`.
The three-argument form (with modulus) is passed as the optional `mod` parameter.

**Signature:**
```python
def __pow__(self, other, mod=None):
    if mod is not None:
        return type(self)(pow(self.value, other, mod))
    return type(self)(self.value ** other)

def __rpow__(self, other):
    return type(self)(other ** self.value)
```

**Called automatically when:**
```python
a ** b          # calls a.__pow__(b)
pow(a, b, mod)  # calls a.__pow__(b, mod)
```

**Relationships:** Reflected: `__rpow__` · In-place: `__ipow__`
"""