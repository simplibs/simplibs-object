class NameNotImplemented:
    """
    Jméno třídy (__name__).

    V SimpleObject: NEIMPLEMENTOVÁNO (automaticky spravováno)
    Důvod: Jméno třídy je nastaveno při její definici.
           Změna by porušila identitu třídy.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__name__` exists on:
- **Modules**: the module's name (`"__main__"` when run directly, otherwise the module name).
- **Classes**: the simple (unqualified) class name — `MyClass.__name__ == "MyClass"`.
- **Functions**: the function's name.
- **NOT on instances**: instances do not have `__name__`.

The classic Python idiom `if __name__ == "__main__":` exploits the fact that Python sets
the executing module's `__name__` to `"__main__"` when it is the entry point.

**You do not define this** — Python sets it. However, you can reassign it (rarely useful
except in frameworks that dynamically create classes).

```python
class MyClass: pass
print(MyClass.__name__)   # "MyClass"   (not "mypackage.MyClass")
print(MyClass.__qualname__)  # "MyClass"   (same for top-level)

# Module-level:
# if __name__ == "__main__":  ← this checks the module's __name__
```

**Relationships:**
- `__qualname__` includes nesting context; `__name__` does not.
- `__module__` tells you *which* module; `__name__` tells you *what it's called* there.
"""