from typing import Any


class BoolMixin:
    """
    Logická hodnota objektu (__bool__).
    Objekt je False, pokud je jeho hodnota None, prázdný string nebo 0.
    """
    __slots__ = ()
    value: Any

    def __bool__(self) -> bool:
        return bool(self.value)


__DOCT__ = """
**Purpose:**
Defines the truthiness of an object — used by `bool(obj)`, `if obj:`, `while obj:`,
and boolean operators (`and`, `or`, `not`). If `__bool__` is not defined, Python falls
back to `__len__` (truthy if non-zero length). If neither is defined, the object is
always truthy (all objects are truthy by default in Python).

**Signature:**
```python
def __bool__(self) -> bool:
    return bool(self.value)   # or some meaningful condition
```

**Called automatically when:**
```python
bool(obj)      # explicit
if obj:        # conditional
not obj        # negation
obj and other  # short-circuit evaluation
```

**Relationships:**
- Fallback chain: `__bool__` → `__len__` → always True.
- Important: for collection-like objects, if `__len__` is defined, you may not need `__bool__`
  because Python automatically considers empty collections falsy.
- Contrast with `__eq__`: equality tests use `__eq__`, truthiness uses `__bool__`.

**Example:**
```python
class BankAccount:
    def __init__(self, balance): self.balance = balance

    def __bool__(self):
        return self.balance > 0   # truthy only if positive balance

account = BankAccount(0)
if not account:
    print("Account is empty!")   # prints this
```
"""