class ClassNotImplemented:
    """
    Odkaz na třídu objektu (__class__).

    V SimpleObject: NEIMPLEMENTOVÁNO (automaticky spravováno)
    Důvod: Python runtime nastavuje __class__ automaticky.
           Manuální změna je nebezpečná a rozbíjí introspekci.
    """
    __slots__ = ()

__DOCT__ = """
**Purpose:**
`__class__` is an auto-attribute present on every instance. It points to the class
(type) that created the instance. It is the same object as `type(instance)` in most
cases, but `__class__` is also used internally by `super()` in the zero-argument form
— Python's compiler injects a hidden `__class__` cell variable into every method that
uses bare `super()`, so that `super()` knows which class it is inside without needing
explicit arguments.

**You do not define this.** Python sets it automatically.

```python
class Animal:
    def speak(self):
        return f"I am a {self.__class__.__name__}"

class Dog(Animal): pass

d = Dog()
print(d.__class__)          # <class '__main__.Dog'>
print(d.__class__ is Dog)   # True
print(type(d) is d.__class__)  # True (in normal cases)
```

**Called automatically when:**
```python
type(instance)        # same object
instance.__class__    # direct attribute access
super()               # zero-argument super() uses the hidden __class__ cell
```

**Relationships:**
- `__class__` cell in methods — hidden by the compiler for `super()` support.
- Distinct from `__classname__` — there is no such thing; use `__class__.__name__`.
- `type(x)` and `x.__class__` differ only when `__class__` has been manually overridden
  (a pattern used by some proxy libraries).
"""