class NewNotImplemented:
    """
    Vytvoření nové instance (__new__).

    V SimpleObject: NEIMPLEMENTOVÁNO (řízeno metaclass)
    Důvod: SimpleObjectMeta řídí alokaci paměti přes __new__.
           Přepisování by rozbilo factory pattern.
    """
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        ...


__DOCT__ = """
**Purpose:**
`__new__` is the *true* constructor of a Python object. It is a static method (though Python
registers it specially so you do not need to decorate it) responsible for allocating and
returning a new instance of the class. It runs *before* `__init__`. Most of the time you
never touch it — Python's default `object.__new__` does the job — but it becomes essential
when subclassing immutable types (`int`, `str`, `tuple`, `frozenset`), implementing the
Singleton pattern, or doing metaclass-level customisation.

**Signature:**
```python
def __new__(cls, *args, **kwargs) -> object:
    instance = super().__new__(cls)
    return instance
```

**Called automatically when:**
```python
obj = MyClass(...)   # Python calls MyClass.__new__(MyClass, ...) first
```

**Relationships:**
- Always paired with `__init__`: `__new__` creates, `__init__` configures.
  If `__new__` returns an instance of a *different* class, `__init__` is NOT called.
- Related to `__init_subclass__` (fires when the class itself is created, not instances).
- Related to `__del__` (the other end of the lifecycle).

**Example:**
```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value   # runs every call, but there's only one instance

a = Singleton(1)
b = Singleton(2)
assert a is b        # True — same object
assert a.value == 2  # __init__ ran twice on the same instance
```
"""