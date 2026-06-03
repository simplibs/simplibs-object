class InstancecheckNotImplemented:
    """
    Metaclass hook pro isinstance() (__instancecheck__).

    V SimpleObject: NEIMPLEMENTOVÁNO (metaclass úroveň)
    Důvod: Přepisování by změnilo chování isinstance() globálně.
           SimpleObjectMeta to nespravuje.
    """
    __slots__ = ()

    def __instancecheck__(self, instance):
        ...


__DOCT__ = """
**Purpose:**
`__instancecheck__` is called by `isinstance(obj, cls)`. Normally `isinstance` checks
the real class hierarchy. By defining `__instancecheck__` on a metaclass, you can make
`isinstance` return `True` for objects that do not actually inherit from your class —
*virtual instances*. This is the mechanism behind `collections.abc`: an object is
"virtually an Iterable" if it has `__iter__`, even without inheriting from `Iterable`.

**It lives on the metaclass, not on the class itself.**

**Signature:**
```python
# On a metaclass:
def __instancecheck__(cls, instance) -> bool:
    return hasattr(instance, "__iter__")   # duck-type check
```

**Called automatically when:**
```python
isinstance(obj, MyClass)   # Python calls type(MyClass).__instancecheck__(MyClass, obj)
```

**Relationships:**
- Companion to `__subclasscheck__` (for `issubclass`).
- Used by `ABCMeta` to implement the virtual subclass / duck-typing protocol.
- `__subclasshook__` (already in your `aaa/` group) is a higher-level API over this.

**Example:**
```python
class DuckMeta(type):
    def __instancecheck__(cls, instance):
        # "if it quacks, it's a Duck"
        return hasattr(instance, "quack") and hasattr(instance, "walk")

class Duck(metaclass=DuckMeta):
    pass

class Robot:
    def quack(self): return "beep"
    def walk(self): return "step step"

print(isinstance(Robot(), Duck))   # True — even though Robot doesn't inherit Duck
```
"""