class DocNotImplemented:
    """
    Dokumentační řetězec třídy (__doc__).

    V SimpleObject: NEIMPLEMENTOVÁNO (automaticky spravováno)
    Důvod: Docstring je nastaven při definici třídy.
           Manuální změna by porušila dokumentaci.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__doc__` holds the docstring of a class, method, function, or module — the string
literal that immediately follows the `def` / `class` statement. Python extracts it
automatically at parse time. It is accessible via `help()`, introspection tools, IDEs,
and documentation generators (Sphinx, pdoc). It can be set to `None` to suppress the
docstring, or assigned a string at class-body level.

**Note for your project:** you use `__DOCT__` as your custom documentation attribute.
`__doc__` is the standard Python attribute that tools like `help()` use; `__DOCT__` is
your own extended documentation field that lives alongside it.

**You can assign it manually:**
```python
class MyClass:
    '''This is the standard docstring.'''     # Python sets __doc__ = "This is..."
    __DOCT__ = '''Extended internal doc.'''   # your custom field
```

**Called automatically when:**
```python
help(MyClass)          # reads __doc__
MyClass.__doc__        # direct access
inspect.getdoc(obj)    # cleaned-up version
```

**Relationships:**
- `__doc__` is writable: `MyClass.__doc__ = "new doc"` is valid.
- `inspect.getdoc()` strips indentation and normalizes whitespace.
- Your `__DOCT__` is a parallel field — not read by `help()` unless you hook into it.
"""