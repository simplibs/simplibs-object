class GetattrNotImplemented:
    """
    Fallback pro přístup k neexistujícím atributům (__getattr__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject používá __slots__ a explicitní atributy.
           Dynamický přístup by porušil předvídatelnost systému.
    """
    __slots__ = ()

    def __getattr__(self, name: str):
        ...



__DOCT__ = """
**Purpose:**
`__getattr__` is a *fallback* — Python only calls it when normal attribute lookup has
failed (i.e., the attribute was not found in the instance dict, the class, or any base
class). This makes it safe to implement without fear of recursion, and ideal for lazy
attributes, dynamic attribute generation, and forward-compatibility shims (returning
defaults for attributes that may be added in the future).

**Signature:**
```python
def __getattr__(self, name: str):
    raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")
```

**Called automatically when:**
```python
obj.nonexistent   # normal lookup fails → __getattr__ is called
```

**Relationships:**
- Only called after `__getattribute__` raises `AttributeError`.
- For writing, the equivalent is `__setattr__`.
- Commonly used alongside `__dir__` to make dynamic attributes discoverable.

**Example:**
```python
class FlexObject:
    def __init__(self):
        self._data = {}

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

obj = FlexObject()
obj.color = "red"
print(obj.color)      # "red" — stored in _data via __setattr__
print(obj.missing)    # AttributeError
```
"""