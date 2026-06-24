class ModuleNotImplemented:
    """
    Jméno modulu kde je třída definována (__module__).

    V SimpleObject: NEIMPLEMENTOVÁNO (automaticky spravováno)
    Důvod: Python nastavuje __module__ při importu.
           Změna by rozbila introspekci a import systém.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__module__` is the name of the module where a class or function was *defined*.
Python sets it automatically from the global `__name__` of the defining module.
Used by `repr()` and `pickle` to locate the class for deserialization (pickle needs
`module.ClassName` to reconstruct an object). For classes defined interactively in
the REPL, it is `"__main__"`.

**You do not define this** — Python sets it. You may read it for introspection
or occasionally override it to control how `repr()` or pickle resolves the class.

```python
# In file: mypackage/models.py
class User:
    pass

print(User.__module__)   # "mypackage.models"
print(repr(User))        # <class 'mypackage.models.User'>
```

**Called automatically when:**
```python
repr(MyClass)          # includes __module__ in the output
pickle.dumps(obj)      # uses __module__ + __qualname__ to locate the class
```

**Relationships:**
- Used with `__qualname__` to form the full dotted path for pickle.
- `__name__` at module level holds the module's own name (not the class's module).
"""