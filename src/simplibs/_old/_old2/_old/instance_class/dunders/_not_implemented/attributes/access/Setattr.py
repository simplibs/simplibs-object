class SetattrNotImplemented:
    """
    Nastavení hodnoty atributu (__setattr__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject řídí změny přes property settery a validaci.
           Přepisování __setattr__ by obešlo validační systém.
    """
    __slots__ = ()

    def __setattr__(self, name: str, value):
        ...


__DOCT__ = """
**Purpose:**
`__setattr__` intercepts *every* attribute assignment on an object — unlike `__getattr__`,
which is only a fallback. This makes it symmetric with `__getattribute__` in its reach.
Use it to validate values, implement read-only attributes, or log all mutations.
**Danger:** inside `__setattr__`, using `self.name = value` will recurse infinitely.
Always use `object.__setattr__(self, name, value)` or `self.__dict__[name] = value`.

**Signature:**
```python
def __setattr__(self, name: str, value) -> None:
    object.__setattr__(self, name, value)   # or self.__dict__[name] = value
```

**Called automatically when:**
```python
obj.x = 10   # calls obj.__setattr__("x", 10)
```

**Relationships:**
- Symmetric counterpart of `__getattribute__` (both intercept everything).
- Works alongside `__delattr__` for attribute deletion.
- Inside `__setattr__`, use `object.__setattr__` to avoid recursion.

**Example:**
```python
class Validated:
    _allowed = {"x", "y"}

    def __setattr__(self, name, value):
        if name not in self._allowed:
            raise AttributeError(f"Cannot set {name!r}")
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be numeric")
        object.__setattr__(self, name, value)

v = Validated()
v.x = 3       # OK
v.x = "bad"   # TypeError
v.z = 1       # AttributeError
```
"""