class NeNotImplemented:
    """
    Operátor nerovnosti (__ne__).

    V SimpleObject: NEIMPLEMENTOVÁNO (automaticky odvozeno)
    Důvod: Od Python 3 se __ne__ automaticky odvozuje z __eq__.
           Explicitní definice je redundantní.
    """
    __slots__ = ()

    def __ne__(self, other):
        ...



__DOCT__ = """
**Purpose:**
`__ne__` defines the `!=` (not-equal) operator. In Python 3, if you define `__eq__`
and do **not** define `__ne__`, Python automatically provides a `__ne__` that returns
`not self.__eq__(other)` (handling `NotImplemented` correctly). This means in practice
you **almost never need to define `__ne__` manually** in Python 3.

It is listed here as an "auto-derived" atom so you know it exists and why it is not
a separate implementation atom in your structure.

The only reason to define `__ne__` manually:
1. You want asymmetric inequality (very rare and usually a design smell).
2. You are writing Python 2-compatible code (Python 2 did NOT auto-derive `__ne__`).
3. Your `__eq__` returns a non-bool type (e.g., a numpy array) and you need custom behaviour.

**Signature (when explicitly needed):**
```python
def __ne__(self, other) -> bool:
    result = self.__eq__(other)
    if result is NotImplemented:
        return result
    return not result
```

**Called automatically when:**
```python
a != b   # calls a.__ne__(b); if NotImplemented → b.__ne__(a)
```

**Relationships:**
- Auto-derived from `__eq__` in Python 3 — define `Eq.py`, get `__ne__` free.
- In Python 2: you had to define both explicitly (Python 2 EOL; noted for historical awareness).
- `__eq__` and `__hash__` are the important pair; `__ne__` just follows along.
"""