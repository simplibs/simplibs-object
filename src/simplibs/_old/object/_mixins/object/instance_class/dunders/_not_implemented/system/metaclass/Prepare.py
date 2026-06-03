class PrepareNotImplemented:
    """
    Metaclass hook pro přípravu class namespace (__prepare__).

    V SimpleObject: NEIMPLEMENTOVÁNO (metaclass úroveň)
    Důvod: SimpleObjectMeta neupravuje namespace při definici třídy.
           Používá __new__ pro konstrukci metadat.
    """
    __slots__ = ()

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        ...


__DOCT__ = """
**Purpose:**
`__prepare__` is a metaclass hook called *before* the class body is executed.
It returns the namespace (dict-like object) that will be used to collect the class body's
definitions. The default returns a plain `dict`. By overriding it you can use an
`OrderedDict`, a custom dict that tracks definition order, or a dict with validation.
This is how Python 3.6+'s `enum.EnumMeta` tracks the order of enum members.

**It lives on the metaclass, not on the class being defined.**

**Signature:**
```python
# On a metaclass:
@classmethod
def __prepare__(mcs, name: str, bases: tuple, **kwargs) -> dict:
    return {}   # or an OrderedDict, or a custom namespace
```

**Called automatically when:**
```python
class MyClass(metaclass=MyMeta):   # __prepare__ fires before the class body runs
    x = 1
    y = 2
```

**Relationships:**
- Called before `__new__` and `__init__` of the metaclass.
- The returned namespace becomes `cls.__dict__` after class creation.
- `__init_subclass__` fires after class creation; `__prepare__` fires before.

**Example:**
```python
class OrderTrackingMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        from collections import OrderedDict
        return OrderedDict()   # track definition order explicitly

class Config(metaclass=OrderTrackingMeta):
    z = 3
    a = 1
    m = 2

print(list(Config.__dict__.keys()))
# ['__module__', '__qualname__', 'z', 'a', 'm', ...]  — order preserved
```
"""