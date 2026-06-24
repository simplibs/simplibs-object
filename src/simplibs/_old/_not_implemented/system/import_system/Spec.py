class SpecNotImplemented:
    """
    ModuleSpec popisující modul (__spec__).

    V SimpleObject: NEIMPLEMENTOVÁNO (import systém)
    Důvod: Nastaveno import systémem při načítání modulu.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__spec__` is a `ModuleSpec` object that Python sets on every imported module. It
contains the full import specification: the module name, origin (file path), loader,
submodule search locations (for packages), and whether the module is a package.
Introduced in Python 3.4 (PEP 451) as part of the import system modernization.

**You do not define this.** `importlib` sets it when a module is imported.

```python
import os
print(os.__spec__)
# ModuleSpec(name='os', origin='/usr/lib/python3.x/os.py', ...)
print(os.__spec__.origin)    # file path
print(os.__spec__.name)      # 'os'
```

**Relationships:**
- Replaces the older `__file__` + `__path__` + `__package__` patchwork.
- `__loader__` and `__package__` are older attributes that `__spec__` supersedes.
- Used by `importlib.util.find_spec()` for import introspection.
"""