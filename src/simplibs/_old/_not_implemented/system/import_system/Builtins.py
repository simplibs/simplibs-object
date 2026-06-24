class BuiltinsNotImplemented:
    """
    Odkaz na vestavěné funkce modulu (__builtins__).

    V SimpleObject: NEIMPLEMENTOVÁNO (import systém)
    Důvod: Spravováno Python import systémem. Změna by rozbila runtime.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__builtins__` is a module-level attribute that Python automatically sets on every
module's global namespace. It points to the `builtins` module (or its `__dict__` in
the `__main__` module — a CPython inconsistency). It is the mechanism by which names
like `len`, `print`, `type`, `None`, `True`, `False` are available without explicit
import in every module.

**You do not define this.** Python's import machinery sets it automatically.

**You might read it in security/sandbox contexts:**
```python
# In a sandboxed eval context, you might restrict __builtins__:
exec(code, {"__builtins__": {}})   # no builtins available in the exec'd code
```

**Relationships:**
- Related to `__spec__`, `__loader__`, `__package__` (all module-level).
- The CPython inconsistency (`__main__` gets `__builtins__.__dict__`, others get the module)
  is a known wart; never rely on its type.
"""