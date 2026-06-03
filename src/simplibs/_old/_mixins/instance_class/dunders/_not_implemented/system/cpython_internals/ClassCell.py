class ClassCellNotImplemented:
    """
    CPython interní struktura pro super() v nested scopes (__class_cell__).

    V SimpleObject: NEIMPLEMENTOVÁNO (CPython implementační detail)
    Důvod: Automaticky spravováno interpretem. Není součást veřejného API.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__class__` cell (sometimes surfaced as `__classcell__`) is a CPython implementation
detail that enables zero-argument `super()`. When Python's compiler sees `super()` inside
a method, it automatically creates a *closure cell* named `__class__` that holds a
reference to the defining class. The metaclass must propagate this cell from the class
namespace to the actual class object, or `super()` will fail.

**You never implement or interact with this** in normal Python code.

If you write a custom metaclass that replaces the class namespace (e.g., in `__prepare__`),
you must ensure `__classcell__` is included in the final class dict or Python will raise
a `DeprecationWarning` (Python 3.6-3.7) or `RuntimeError` (Python 3.8+).

```python
# If you write a custom metaclass with __prepare__:
class MyMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        # DO NOT discard namespace['__classcell__'] if present
        return super().__new__(mcs, name, bases, namespace)
```

**Relationships:**
- Linked to `__class__` auto-attribute and `super()` built-in.
- Only relevant when writing metaclasses that manipulate the class namespace.
"""