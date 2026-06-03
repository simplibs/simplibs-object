# lifecycle/class_hooks/ClassGetitem.py
class ClassGetitemMixin:
    __slots__ = ()
    def __class_getitem__(cls, item):
        # Umožňuje zápis MyClass[int] pro generics / type hints
        # Základní implementace vrací GenericAlias
        return type(cls).__class_getitem__(cls, item) if hasattr(type(cls), "__class_getitem__") else cls


__DOCT__ = """
**Purpose:**
`__class_getitem__` enables the subscript syntax `MyClass[SomeType]` at the *class* level
(not on instances). This is how Python's generic types work: `list[int]`, `dict[str, int]`,
`Optional[str]`. Without this method, `MyClass[...]` raises `TypeError`. It should return a
`GenericAlias` or similar object that carries the type information.

**Signature:**
```python
@classmethod
def __class_getitem__(cls, item):
    return ...   # typically a GenericAlias
```

**Called automatically when:**
```python
MyClass[int]      # Python calls MyClass.__class_getitem__(int)
MyClass[str, int] # Python calls MyClass.__class_getitem__((str, int))
```

**Relationships:**
- Sibling of `__init_subclass__` — both are class-level hooks.
- Used heavily with `typing` module generics.
- `__getitem__` is its *instance-level* counterpart.

**Example:**
```python
from types import GenericAlias

class Stack:
    def __class_getitem__(cls, item):
        return GenericAlias(cls, item)

# Now usable as a generic type hint
def process(stack: Stack[int]) -> None:
    pass

print(Stack[int])  # stack.Stack[int]
```
"""