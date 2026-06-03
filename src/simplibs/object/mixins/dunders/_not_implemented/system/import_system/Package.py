class PackageNotImplemented:
    """
    Jméno package obsahujícího modul (__package__).

    V SimpleObject: NEIMPLEMENTOVÁNO (import systém)
    Důvod: Nastaveno import systémem pro relativní importy.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__package__` is a string set on every module that indicates the module's *package*
context. For a module `mypackage.submodule`, `__package__` is `"mypackage"`.
For a top-level module, it is `""` (empty string). For `__main__`, it is `None` unless
run as part of a package (`python -m mypackage.script`).

Used by relative imports (`.` and `..` syntax) to resolve the package context.

**You do not define this.** The import machinery sets it.

```python
# In mypackage/utils.py:
# __package__ == "mypackage"
# from . import other   ← uses __package__ to resolve the relative import
```

**Relationships:**
- `__name__` is the full module name; `__package__` is just the package part.
- `__spec__.parent` is the modern equivalent.
- Required for relative imports to work correctly.
"""