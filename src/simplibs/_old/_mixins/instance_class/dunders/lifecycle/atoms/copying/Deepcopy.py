# lifecycle/copying/Deepcopy.py
import copy as _copy
class DeepcopyMixin:
    __slots__ = ()
    def __deepcopy__(self, memo):
        # Hluboká kopie hodnoty
        return self.__class__(_copy.deepcopy(self.value, memo))

__DOCT__ = """
**Purpose:**
`__deepcopy__` defines what happens when `copy.deepcopy(obj)` is called — a *deep* copy.
Every nested object is recursively cloned, producing a fully independent object graph.
The `memo` dict argument is used internally by the copy machinery to handle circular
references (if an object appears twice in the graph, it is only copied once).

**Signature:**
```python
def __deepcopy__(self, memo: dict):
    import copy
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        setattr(result, k, copy.deepcopy(v, memo))
    return result
```

**Called automatically when:**
```python
import copy
new_obj = copy.deepcopy(obj)   # calls obj.__deepcopy__(memo)
```

**Relationships:**
- Paired with `__copy__` (shallow variant).
- The `memo` dict is shared across the whole deep-copy operation — always use it.
- If not defined, Python uses `__reduce_ex__` as a fallback.

**Example:**
```python
import copy

class Node:
    def __init__(self, value, children=None):
        self.value    = value
        self.children = children or []

    def __deepcopy__(self, memo):
        new = Node(self.value)
        memo[id(self)] = new
        new.children = copy.deepcopy(self.children, memo)
        return new

root = Node(1, [Node(2), Node(3)])
clone = copy.deepcopy(root)
clone.children[0].value = 99
print(root.children[0].value)   # 2 — original is untouched
```
"""