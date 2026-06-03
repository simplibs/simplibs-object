class SubclasshookNotImplemented:
    """
    Hook pro ABC virtuální podtřídy (__subclasshook__).

    V SimpleObject: NEIMPLEMENTOVÁNO (ABC systém)
    Důvod: SimpleObject nepoužívá ABC virtual subclass systém.
    """
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, subclass):
        ...



__DOCT__ = """
**Purpose:**
`__subclasshook__` is a class method on `ABCMeta`-based abstract classes that customizes
the `issubclass()` check. Returning `True` makes Python treat a class as a *virtual*
subclass of the ABC — without it actually inheriting from it. This is how `collections.abc`
works: a class that defines `__len__` and `__getitem__` is recognized as a `Sequence`
without inheriting from `Sequence`.

**Signature:**
```python
@classmethod
def __subclasshook__(cls, subclass) -> bool:
    if cls is MyABC:
        if hasattr(subclass, "required_method"):
            return True
    return NotImplemented
```

**Called automatically when:**
```python
issubclass(SomeClass, MyABC)   # Python calls MyABC.__subclasshook__(SomeClass)
isinstance(obj, MyABC)         # also triggers subclasshook
```

**Relationships:**
- Only meaningful in `ABCMeta`-based classes.
- Works alongside `__abstractmethods__`.
- `NotImplemented` (not `False`) means "use normal subclass check".
"""

