from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class ModMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __mod__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value % other_value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    def __rmod__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value % self.value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements the `%` modulo operator. Also used by `str` for old-style `"Hello %s" % name`
formatting. The result has the same sign as the divisor (not the dividend).

**Signature:**
```python
def __mod__(self, other):
    return type(self)(self.value % other)

def __rmod__(self, other):
    return type(self)(other % self.value)
```

**Called automatically when:**
```python
a % b
```

**Relationships:** Reflected: `__rmod__` · In-place: `__imod__`
"""