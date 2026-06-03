# lifecycle/copying/Reduce.py
class ReduceMixin:
    __slots__ = ()
    def __reduce__(self):
        # Kompaktní pickle protokol
        return (self.__class__, (self.value,))

__DOCT__ = """
**Purpose:**
`__reduce__` defines how an object is serialized by the `pickle` module. It must return
either a string (global name) or a tuple of `(callable, args[, state[, list_items[, dict_items]]])`.
The callable and args must be importable at the top level so the pickle machinery can
reconstruct the object. This is the lower-level interface; `__reduce_ex__` is preferred.

**Signature:**
```python
def __reduce__(self):
    return (self.__class__, (self.value,))
```

**Called automatically when:**
```python
import pickle
data = pickle.dumps(obj)   # invokes __reduce__ (or __reduce_ex__)
```

**Relationships:**
- `__reduce_ex__` takes a protocols version argument and is called first; it falls back to `__reduce__`.
- `__getstate__` / `__setstate__` are a higher-level, often cleaner alternative.
- `__copy__` / `__deepcopy__` also fall back to `__reduce_ex__` if not defined.

**Example:**
```python
import pickle

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __reduce__(self):
        return (Point, (self.x, self.y))

p = Point(3, 4)
data  = pickle.dumps(p)
clone = pickle.loads(data)
print(clone.x, clone.y)   # 3  4
```
"""