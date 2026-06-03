# lifecycle/copying/Copy.py
class CopyMixin:
    __slots__ = ()
    def __copy__(self):
        # Mělká kopie — nová instance se stejnou hodnotou
        return self.__class__(self.value)

__DOCT__ = """
**Purpose:**
`__copy__` defines what happens when `copy.copy(obj)` is called — a *shallow* copy.
A shallow copy creates a new object of the same type but does not recursively copy
nested objects; references to inner objects are shared. If you do not define `__copy__`,
Python falls back to `__reduce_ex__` / `__reduce__`.

**Signature:**
```python
def __copy__(self):
    cls = self.__class__
    result = cls.__new__(cls)
    result.__dict__.update(self.__dict__)
    return result
```

**Called automatically when:**
```python
import copy
new_obj = copy.copy(obj)   # calls obj.__copy__()
```

**Relationships:**
- Paired with `__deepcopy__` for full recursive cloning.
- Falls back to `__reduce_ex__` if not defined.
- Contrast: `__getstate__` / `__setstate__` control pickle state.

**Example:**
```python
import copy

class Config:
    def __init__(self, data: dict):
        self.data = data

    def __copy__(self):
        new = Config(self.data)   # shares the same dict reference
        return new

c1 = Config({"key": [1, 2, 3]})
c2 = copy.copy(c1)
c2.data["key"].append(4)
print(c1.data["key"])   # [1, 2, 3, 4] — shared reference!
```
"""