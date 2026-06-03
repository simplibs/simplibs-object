"""
comparison/equality/Eq.py ⚠️
Současný kód:
pythonclass EqMixin(HashMixin):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return self.value == other
PROBLÉM: EqMixin(HashMixin) je obrácené dědění.
V Pythonu platí: "Objects which compare equal must have the same hash."
Pokud přepíšeš __eq__, musíš přepsat i __hash__, nebo nastavit __hash__ = None.
Správná struktura:
pythonclass HashMixin:
    def __hash__(self):
        try:
            return hash(self.value)
        except TypeError:
            return id(self)

class EqMixin(HashMixin):  # NEBO: class EqMixin:
    def __eq__(self, other):
        ...
```

**Doporučení:**
Nechat `HashMixin` jako samostatný atom.
`EqMixin` **nedědí** z `HashMixin`, ale jsou často používány dohromady.

Nebo vytvořit:
- `EqMixin` — jen `__eq__`
- `HashableEqMixin(EqMixin, HashMixin)` — kombinace

**A přesunout složku `hash/` mimo `comparison/`, protože `__hash__` není porovnávací operátor.**

Navrhuji:
```
comparison/
  equality/
    Eq.py
    Ne.py (vysvětlit proč not_implemented)
  ordering/
    Lt.py, Le.py, Gt.py, Ge.py
identity/
  Hash.py
comparison/hash/Hash.py — přesunout do identity/
"""

from typing import Any


class EqMixin:
    """
    Rovnost objektů (__eq__).
    Porovnává vnitřní hodnotu a podporuje i porovnání s primitivními hodnotami.
    """
    __slots__ = ()
    value: Any

    def __eq__(self, other: Any) -> bool:
        # Stejná třída nebo potomek
        if isinstance(other, self.__class__):
            return self.value == other.value

        # Porovnání s hodnotou přímo
        return self.value == other



__DOCT__ = """
**Purpose:**
Defines `==` comparison. The default implementation (from `object`) compares by identity
(`self is other`), which is almost never what you want for value objects. Override it to
compare by meaningful attributes. **Critical side-effect:** defining `__eq__` automatically
sets `__hash__` to `None`, making your object unhashable unless you also define `__hash__`.

**Signature:**
```python
def __eq__(self, other) -> bool:
    if not isinstance(other, type(self)):
        return NotImplemented
    return self.value == other.value
```

**Called automatically when:**
```python
a == b   # calls a.__eq__(b); if NotImplemented → b.__eq__(a)
```

**Relationships:**
- **Inseparable from `__hash__`**: if you define `__eq__`, you must decide what to do with `__hash__`.
  If objects that compare equal must hash equal (the rule for dict keys / sets), define `__hash__`
  to match. If unhashable is OK, set `__hash__ = None` explicitly.
- `__ne__` is automatically the negation of `__eq__` in Python 3.
- Related to `__lt__` etc. for ordering.

**Example:**
```python
class Point:
    def __init__(self, x, y): self.x, self.y = x, y
    def __eq__(self, other):
        if not isinstance(other, Point): return NotImplemented
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))   # must define since we defined __eq__

p1, p2 = Point(1, 2), Point(1, 2)
print(p1 == p2)          # True
print({p1, p2})          # {Point} — only one element because equal ⇒ same hash
```
"""