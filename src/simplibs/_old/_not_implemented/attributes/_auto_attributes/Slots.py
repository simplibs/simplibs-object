class SlotsNotImplemented:
    """
    Tuple explicitních atributů (__slots__).

    V SimpleObject: NEIMPLEMENTOVÁNO (definováno při tvorbě třídy)
    Důvod: __slots__ je deklarováno při definici třídy v SimpleBase.
           Dynamická změna není možná po vytvoření třídy.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__slots__` is a class-level declaration (not a method) that replaces the per-instance
`__dict__` with a fixed set of slot descriptors. Benefits: lower memory per instance
(no dict overhead), faster attribute access (direct offset instead of hash lookup),
prevents accidental attribute creation. Downsides: inheritance is tricky (all classes
in the chain must define `__slots__`), and you lose flexibility.

**You do not implement this** — you declare it:
```python
class Point:
    __slots__ = ("x", "y")   # no __dict__, only x and y allowed
    def __init__(self, x, y): self.x, self.y = x, y

p = Point(1, 2)
p.z = 3   # AttributeError — no __dict__, no z slot
```

**Relationships:**
- Eliminates `__dict__`, so `vars(instance)` raises `TypeError`.
- `__weakref__` must be added to `__slots__` explicitly if you need weak references.
- Each slot is internally a data descriptor on the class.
"""
