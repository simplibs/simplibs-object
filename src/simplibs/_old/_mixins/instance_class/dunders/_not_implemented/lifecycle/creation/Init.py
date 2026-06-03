class InitNotImplemented:
    """
    Inicializace nové instance (__init__).

    V SimpleObject: NEIMPLEMENTOVÁNO (dynamicky generováno)
    Důvod: make_atomic_instance() dynamicky vytváří __init__ s parametry
           podle metadat (param_map, inners) a generuje signatury pro IDE.
    """
    __slots__ = ()

    def __init__(self, **kwargs):
        ...



__DOCT__ = """
**Purpose:**
`__init__` is the *initializer* — it receives the already-created instance (produced by
`__new__`) and populates it with initial state. It is the method most Python programmers
think of as "the constructor". It must return `None`; returning anything else raises
`TypeError`. It is the right place for setting instance attributes, validating arguments,
and wiring up dependencies.

**Signature:**
```python
def __init__(self, *args, **kwargs) -> None:
    self.value = args[0]
```

**Called automatically when:**
```python
obj = MyClass(42)   # Python calls obj.__init__(42) after __new__
```

**Relationships:**
- Runs after `__new__`. If `__new__` returns a foreign type, `__init__` is skipped.
- Contrasted with `__new__`: you override `__init__` for mutable types; `__new__` for immutable ones.
- `__del__` is its counterpart at end-of-life.

**Example:**
```python
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

v = Vector(3.0, 4.0)
print(v.x, v.y)   # 3.0  4.0
```
"""