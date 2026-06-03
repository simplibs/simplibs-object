from .Ge import GeMixin
from .Gt import GtMixin
from .Le import LeMixin
from .Lt import LtMixin
from .LtLeGtGe import LtLeGtGeMixin

__all__ = (
    "GeMixin",
    "GtMixin",
    "LeMixin",
    "LtMixin",
    "LtLeGtGeMixin",
)


"""
comparison/ordering/Lt.py, Le.py, Gt.py, Ge.py ⚠️
Současný stav: Jeden soubor LtLeGtGe.py s @total_ordering.
Otázka: Rozdělit na 4 samostatné atomy?
Analýza @total_ordering:
pythonfrom functools import total_ordering

@total_ordering
class C:
    def __eq__(self, other): ...
    def __lt__(self, other): ...
    # __le__, __gt__, __ge__ se VYGENERUJÍ
Vygenerované metody vypadají přesně takto:
pythondef __le__(self, other):
    return self == other or self < other

def __gt__(self, other):
    return not (self < other or self == other)

def __ge__(self, other):
    return not (self < other)
Závěr: Logika je velmi jednoduchá. Můžeš rozdělit na 4 samostatné atomy:
python# ordering/Lt.py
class LtMixin:
    def __lt__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value < other_value
        except TypeError:
            return NotImplemented

# ordering/Le.py
class LeMixin:
    # Varianta 1: Využít Lt + Eq (vyžaduje oba mixiny)
    def __le__(self, other):
        return self == other or self < other

    # Varianta 2: Samostatná logika
    def __le__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value <= other_value
        except TypeError:
            return NotImplemented

# ordering/Gt.py
class GtMixin:
    def __gt__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value > other_value
        except TypeError:
            return NotImplemented

# ordering/Ge.py
class GeMixin:
    def __ge__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self.value >= other_value
        except TypeError:
            return NotImplemented
Doporučení:
Rozdělit na 4 atomy s přímou logikou (bez závislostí na < + ==). Proč?

Atomická struktura
Uživatel může chtít jen < bez <=
Některé typy implementují <= efektivněji než < or ==

A zachovat LtLeGtGe.py jako composition mixin (přesunout do composition/ordering/Orderable.py).
"""

__DOCT__ = """
## `comparison/ordering/`

> **Subgroup purpose:**
> The four ordering operators. You only need to implement all four if you cannot use
> `functools.total_ordering` — that decorator lets you define just `__eq__` and one of
> the four, and it derives the rest. Implement all four manually when performance matters
> or when the derivation is not straightforward.
"""