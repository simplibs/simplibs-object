class MroEntriesNotImplemented:
    """
    Hook pro úpravu MRO při dědění (__mro_entries__).

    V SimpleObject: NEIMPLEMENTOVÁNO (metaclass úroveň)
    Důvod: SimpleObjectMeta řídí MRO. Přidání __mro_entries__ by
           kolidovalo s mixinovým systémem.
    """
    __slots__ = ()

    def __mro_entries__(self, bases):
        ...


__DOCT__ = """
**Purpose:**
`__mro_entries__` is called by Python's type system when a *non-class* object appears
in a class's bases tuple. It must return a tuple of actual classes to substitute for
that object in the MRO (Method Resolution Order) computation. This is used by PEP 560
to enable generic aliases like `list[int]` to appear as base classes.

**Signature:**
```python
def __mro_entries__(self, bases: tuple) -> tuple:
    return (self.__origin__,)   # return the actual class to inherit from
```

**Called automatically when:**
```python
class MyList(list[int]):   # list[int] is a GenericAlias; __mro_entries__ is called
    pass
```

**Relationships:**
- Enables PEP 585 generic types (`list[int]`, `dict[str, int]`) as base classes.
- Companion to `__class_getitem__` (which creates the generic alias in the first place).
- Rarely implemented outside of typing infrastructure.
"""

