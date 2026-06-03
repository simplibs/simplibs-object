# lifecycle/copying/Setstate.py
class SetstateMixin:
    __slots__ = ()
    def __setstate__(self, state):
        # Pro pickle — obnovíme hodnotu ze stavu
        self.value = state["value"]

__DOCT__ = """
**Purpose:**
`__setstate__` is the counterpart of `__getstate__`. It receives the state dict that was
saved and is responsible for restoring the object's attributes. It is called on a freshly
created (but uninitialized) instance during unpickling. This is where you handle schema
migrations — if old pickled data is missing a new field, you can add a default here.

**Signature:**
```python
def __setstate__(self, state: dict) -> None:
    state.setdefault("version", 1)   # migration default
    self.__dict__.update(state)
```

**Called automatically when:**
```python
import pickle
obj = pickle.loads(data)   # calls __setstate__(state) on the new instance
```

**Relationships:**
- Always paired with `__getstate__`.
- Runs after `__new__` but instead of `__init__` during unpickling.

---
"""