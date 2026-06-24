class QualnameNotImplemented:
    """
    Kvalifikované jméno třídy (__qualname__).

    V SimpleObject: NEIMPLEMENTOVÁNO (automaticky spravováno)
    Důvod: __qualname__ zahrnuje vnořené třídy a je spravován Pythonem.
           Manuální změna by porušila import systém.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__qualname__` (qualified name) is the dotted path from the *enclosing scope* to the
class or function. For top-level classes it equals `__name__`. For nested classes it
includes the outer class: `"Outer.Inner"`. For methods it is `"MyClass.my_method"`.
Introduced in Python 3.3 (PEP 3155) primarily to make `repr()` and pickle more
informative for nested definitions.

**You do not define this** — Python sets it at class/function creation time.

```python
class Outer:
    class Inner:
        pass

print(Outer.__qualname__)        # "Outer"
print(Outer.Inner.__qualname__)  # "Outer.Inner"

def outer():
    def inner(): pass
    return inner

f = outer()
print(f.__qualname__)   # "outer.<locals>.inner"
```

**Relationships:**
- Together with `__module__`, uniquely identifies a class for pickle.
- `__name__` is just the bare name without nesting context.
- Used by `repr()`, `inspect`, and debugging tools.
"""