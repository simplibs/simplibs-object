class WeakrefNotImplemented:
    """
    Slot pro weak references (__weakref__).

    V SimpleObject: NEIMPLEMENTOVÁNO (součást __slots__)
    Důvod: Pokud je potřeba weak reference, přidá se do __slots__.
           Není to dunder metoda, ale atribut.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__weakref__` is an automatic attribute (added by Python to any class that has a `__dict__`)
that enables *weak references* — references that do not prevent garbage collection.
When using `__slots__`, you must explicitly include `"__weakref__"` in the slots tuple
to preserve this capability. Used by `weakref.ref()`, `weakref.WeakValueDictionary`, etc.

**You do not implement this** — Python manages it. The only action needed is:
```python
class MyClass:
    __slots__ = ("x", "__weakref__")   # explicitly preserve weakref support
```

**Relationships:**
- Automatically present when `__dict__` is present.
- Must be declared in `__slots__` for slotted classes.
- Used by `weakref`, caches, event systems, and observer patterns.
"""
# __weakref__ — automatický atribut