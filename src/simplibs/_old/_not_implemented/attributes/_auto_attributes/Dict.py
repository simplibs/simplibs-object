class DictNotImplemented:
    """
    Slovník atributů instance (__dict__).

    V SimpleObject: NEIMPLEMENTOVÁNO (konflikty s __slots__)
    Důvod: SimpleObject používá __slots__ pro efektivitu paměti.
           __dict__ a __slots__ se vzájemně vylučují.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__dict__` is not a method — it is an automatically created attribute that stores the
instance's namespace (a dictionary of attribute names → values). It is present on all
ordinary instances (unless `__slots__` is used). You rarely need to interact with it
directly, though it is useful for introspection, serialization (`__getstate__` often
returns a copy of `__dict__`), and merging attribute sets.

**You do not define this** — Python creates it automatically. You interact with it via
`instance.__dict__`, `vars(instance)`, or indirectly through `__getattribute__`.

**Relationships:**
- `__slots__` replaces `__dict__` with a fixed-layout structure (no per-instance dict).
- `__getstate__` often returns `self.__dict__.copy()`.
- `__setattr__` can write to `self.__dict__[name]` directly to bypass the setter.
"""
