from typing import Any
from ..equality.Eq import EqMixin


class HashMixin(EqMixin):
    """
    Umožňuje použití objektu v setech nebo jako klíče v dict (__hash__).
    """
    __slots__ = ()
    value: Any

    def __hash__(self) -> int:
        try:
            return hash(self.value)
        except TypeError:
            # fallback pro nemutovatelné hodnoty
            return id(self)



__DOCT__ = """
**Purpose:**
Defines the hash value of an object — an integer used by `dict` and `set` for bucket
lookup. Must be consistent: `a == b` implies `hash(a) == hash(b)`. The reverse is not
required (hash collisions are normal). **Python rule:** if you define `__eq__`, Python
sets `__hash__ = None` (unhashable) unless you explicitly define `__hash__`. Mutable
objects should typically be unhashable (like `list`) because mutation would silently
corrupt dict/set invariants.

**Signature:**
```python
def __hash__(self) -> int:
    return hash((self.x, self.y))   # hash a tuple of identifying attributes
```

**Called automatically when:**
```python
hash(obj)        # explicit
d = {obj: 1}     # dict key lookup
s = {obj}        # set membership
```

**Relationships:**
- Inseparable from `__eq__`: must define together.
- Mutable containers (`list`, `dict`) deliberately set `__hash__ = None`.
- `functools.cached_property` and `@cache` rely on hashable objects.

**Example:**
```python
class FrozenPair:
    def __init__(self, a, b): self.a, self.b = a, b
    def __eq__(self, other): return (self.a, self.b) == (other.a, other.b)
    def __hash__(self): return hash((self.a, self.b))

pairs = {FrozenPair(1, 2), FrozenPair(1, 2), FrozenPair(3, 4)}
print(len(pairs))   # 2 — the two equal FrozenPairs merged into one
```
"""