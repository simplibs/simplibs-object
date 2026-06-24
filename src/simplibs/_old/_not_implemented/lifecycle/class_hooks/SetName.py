class SetNameNotImplemented:
    """
    Hook volaný když je descriptor přiřazen k atributu (__set_name__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject není descriptor.
           __set_name__ se používá pro descriptor protokol.
    """
    __slots__ = ()

    def __set_name__(self, owner, name):
        ...



__DOCT__ = """
**Purpose:**
`__set_name__` is called on a *descriptor* object at the moment the class that *owns* it
is being defined. It receives the owner class and the attribute name under which the
descriptor was assigned. This lets a descriptor know its own name without the user having
to specify it redundantly, enabling cleaner descriptor implementations.

**Signature:**
```python
def __set_name__(self, owner: type, name: str) -> None:
    self.name = name
    self.private_name = f"_{name}"
```

**Called automatically when:**
```python
class MyClass:
    x = MyDescriptor()   # __set_name__(MyClass, "x") is called here
```

**Relationships:**
- Works in tandem with `__get__`, `__set__`, `__delete__` (the descriptor protocol).
- Part of class-definition-time hooks alongside `__init_subclass__`.

**Example:**
```python
class ValidatedField:
    def __set_name__(self, owner, name):
        self.public_name  = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.public_name} must be int")
        setattr(obj, self.private_name, value)

class Record:
    age = ValidatedField()   # __set_name__ fires here automatically

r = Record()
r.age = 30   # OK
r.age = "x"  # TypeError: age must be int
```
"""