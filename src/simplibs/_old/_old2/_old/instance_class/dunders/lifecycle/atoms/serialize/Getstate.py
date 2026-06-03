# lifecycle/copying/Getstate.py
class GetstateMixin:
    __slots__ = ()
    def __getstate__(self):
        # Pro pickle — vrátíme hodnotu jako stav
        return {"value": self.value}

__DOCT__ = """
**Purpose:**
`__getstate__` returns the object's *serializable state* — typically a dict — which pickle
will store. If your object contains non-picklable attributes (locks, file handles, sockets),
you can exclude them here. It also lets you add migration metadata (e.g., a version field)
to help `__setstate__` handle old pickled data.

**Signature:**
```python
def __getstate__(self) -> dict:
    state = self.__dict__.copy()
    state.pop("_lock", None)   # remove non-picklable
    return state
```

**Called automatically when:**
```python
import pickle
pickle.dumps(obj)   # calls __getstate__() to capture state
```

**Relationships:**
- Always paired with `__setstate__` (restore) for a complete pickle customisation.
- Called internally by `__reduce_ex__`'s default implementation.
- Related to `__copy__` / `__deepcopy__` via the pickle fallback path.

**Example:**
```python
import pickle, threading

class Worker:
    def __init__(self, name):
        self.name = name
        self._lock = threading.Lock()   # not picklable!

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._lock = threading.Lock()   # recreate after unpickling

w  = Worker("builder")
w2 = pickle.loads(pickle.dumps(w))
print(w2.name)   # "builder" — lock was excluded and recreated
```

"""