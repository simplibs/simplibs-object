from typing import Any


class LenMixin:
    """
    Vrací počet vnitřních prvků.
    """

    # Očekává
    meta: Any

    def __len__(self) -> int:
        """Počet vnitřních prvků."""
        return len(self.meta.inners) if self.meta.inners else 0


__DOCT__ = """
**Purpose:**
Defines `len(obj)`. Must return a non-negative integer. Python uses this for:
truthiness evaluation (if `__bool__` is absent, empty = falsy), internal optimizations
in iteration, and validation (slicing, etc.). Raising an error from `__len__` is valid
(e.g., for lazy containers whose length is unknown).

**Signature:**
```python
def __len__(self) -> int:
    return len(self._data)
```

**Called automatically when:**
```python
len(obj)          # explicit
bool(obj)         # fallback if __bool__ not defined
# also used internally by Python for various optimisations
```

**Relationships:**
- Fallback for `__bool__` if `__bool__` is not defined.
- Required by the Sequence and Mapping abstract base classes.
- Works alongside `__getitem__` — together they form the minimum Sequence protocol.

**Example:**
```python
class Pipeline:
    def __init__(self): self._steps = []
    def add(self, step): self._steps.append(step)
    def __len__(self): return len(self._steps)

p = Pipeline()
print(len(p))     # 0
p.add("step1")
print(bool(p))    # True — len > 0 → truthy
```
"""