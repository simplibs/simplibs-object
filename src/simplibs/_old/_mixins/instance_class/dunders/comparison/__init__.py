from .Equality import EqualityMixin
from .Orderable import OrderableMixin
from .Comparable import ComparableMixin

__all__ = (
    "EqualityMixin",
    "OrderableMixin",
    "ComparableMixin",
)


# # comparison/__init__.py
#
# # 1. Equality — jen rovnost
# class Equality(EqMixin):
#     """Podporuje == (a automaticky !=)"""
#     __slots__ = ()
#
# # 2. Orderable — plné uspořádání
# class Orderable(LtMixin, LeMixin, GtMixin, GeMixin):
#     """Podporuje <, <=, >, >="""
#     __slots__ = ()
#
# # 3. Comparable — rovnost + uspořádání
# class Comparable(EqMixin, LtMixin, LeMixin, GtMixin, GeMixin):
#     """Podporuje ==, <, <=, >, >="""
#     __slots__ = ()
#
#
# # **Otázka:** Potřebujeme `Comparable`? Nebo stačí kombinovat `Equality + Orderable`?
# # **Odpověď:** `Comparable` je užitečné jako **jeden import** pro "plně porovnatelný objekt". Nechal bych ho.
#
# __DOCT__ = """
# # GROUP: `comparison/`
#
# > **Group purpose:**
# > How objects compare to each other. Python's comparison model is rich:
# > equality (`==`), identity (`is`), ordering (`<`, `>`, etc.), and hashing (required for
# > dict keys and set membership). These dunders form interdependent pairs and triads —
# > notably, `__eq__` and `__hash__` are inseparably linked by Python's data model.
# """