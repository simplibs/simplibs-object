class SubclasscheckNotImplemented:
    """
    Metaclass hook pro issubclass() (__subclasscheck__).

    V SimpleObject: NEIMPLEMENTOVÁNO (metaclass úroveň)
    Důvod: Přepisování by změnilo chování issubclass() globálně.
           SimpleObjectMeta to nespravuje.
    """
    __slots__ = ()

    def __subclasscheck__(self, subclass):
        ...


__DOCT__ = """
**Purpose:**
`__subclasscheck__` is the metaclass hook for `issubclass(sub, cls)`. It lets you define
what it means for one class to be a "subclass" of another without requiring actual
inheritance. Companion to `__instancecheck__`. Used internally by `ABCMeta` to implement
virtual subclass registration via `ABC.register()`.

**It lives on the metaclass.**

**Signature:**
```python
# On a metaclass:
def __subclasscheck__(cls, subclass) -> bool:
    return hasattr(subclass, "required_method")
```

**Called automatically when:**
```python
issubclass(SubClass, MyClass)  # calls type(MyClass).__subclasscheck__(MyClass, SubClass)
```

**Relationships:**
- Companion to `__instancecheck__`.
- `__subclasshook__` (in your `aaa/` group) is the `ABCMeta`-specific higher-level API.
- Together, `__instancecheck__` + `__subclasscheck__` form the full isinstance/issubclass customisation pair.
"""