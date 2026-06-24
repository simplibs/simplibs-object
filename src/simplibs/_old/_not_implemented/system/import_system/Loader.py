class LoaderNotImplemented:
    """
    Loader použitý pro import modulu (__loader__).

    V SimpleObject: NEIMPLEMENTOVÁNO (import systém)
    Důvod: Nastaveno import systémem při načítání modulu.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__loader__` is the loader object that loaded the module — typically a
`SourceFileLoader`, `SourcelessFileLoader`, or `BuiltinImporter`. It is part of the
import system protocols (PEP 302, PEP 451) and is set automatically on modules.
Loaders implement methods like `get_source()`, `get_code()`, and `exec_module()`.

**You do not define this on normal classes.** It is set by `importlib` on module objects.

```python
import json
print(json.__loader__)        # <SourceFileLoader 'json' '/path/to/json/__init__.py'>
print(json.__loader__.get_source("json"))  # returns the source code as a string
```

**Relationships:**
- Part of the triple: `__spec__`, `__loader__`, `__package__`.
- `__spec__.loader` is the modern way to access the same object.
"""