class DelattrNotImplemented:
    """
    Smazání atributu objektu (__delattr__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject používá __slots__ a immutable-by-default filozofii.
           Mazání atributů by porušilo validační systém.
    """
    __slots__ = ()

    def __delattr__(self, name: str):
        ...


__DOCT__ = """
**Purpose:**
`__delattr__` intercepts `del obj.name` statements. Like `__setattr__`, it fires for every
deletion attempt, not just missing attributes. Use it to prevent deletion of critical
attributes, to log deletions, or to trigger side effects (e.g., invalidating a cache)
when an attribute is removed.

**Signature:**
```python
def __delattr__(self, name: str) -> None:
    object.__delattr__(self, name)   # default behaviour
```

**Called automatically when:**
```python
del obj.x   # calls obj.__delattr__("x")
```

**Relationships:**
- Completes the attribute triad: `__getattribute__`, `__setattr__`, `__delattr__`.
- If combined with `__setattr__`, you have full control over the attribute lifecycle.

**Example:**
```python
class Protected:
    def __init__(self, name, locked):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "_locked", set(locked))

    def __delattr__(self, name):
        if name in self._locked:
            raise AttributeError(f"Cannot delete protected attribute {name!r}")
        object.__delattr__(self, name)

p = Protected("item", locked=["name"])
del p.name   # AttributeError: Cannot delete protected attribute 'name'
```
"""