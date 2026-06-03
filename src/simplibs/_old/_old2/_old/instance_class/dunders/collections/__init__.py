from .Container import ContainerMixin
from .Iterable import IterableMixin
from .Reversible import ReversibleMixin
from .Inspectable import InspectableMixin
from .Mapping import MappingMixin
from .MutableMapping import MutableMappingMixin
from .MappingView import MappingViewMixin

__all__ = (
    "ContainerMixin",
    "IterableMixin",
    "ReversibleMixin",
    "InspectableMixin",
    "MappingMixin",
    "MutableMappingMixin",
    "MappingViewMixin",
)



# # collections/__init__.py
#
# # 1. Container — základní kontejnerové chování
# class Container(ContainsMixin, LenMixin):
#     """Objekt který umí `in` a `len()`"""
#     __slots__ = ()
#
# # 2. Iterable — základní iterace
# class Iterable(IterMixin):
#     """Objekt který umí `for x in obj`"""
#     __slots__ = ()
#
# # 3. Reversible — iterace + reverse
# class Reversible(IterMixin, ReversedMixin):
#     """Objekt který umí `for x in reversed(obj)`"""
#     __slots__ = ()
#
# # 4. Mapping — read-only mapping
# class Mapping(GetitemMixin, IterMixin, LenMixin, ContainsMixin):
#     """Read-only mapping (obj['key'], len, in, iteration)"""
#     __slots__ = ()
#
# # 5. MutableMapping — read-write mapping
# class MutableMapping(SetitemMixin, GetitemMixin, IterMixin, LenMixin, ContainsMixin):
#     """Mutable mapping (obj['key'] = value)"""
#     __slots__ = ()
#
# # 6. MappingView — Mapping + views (items, keys, values)
# class MappingView(GetitemMixin, IterMixin, LenMixin, ContainsMixin, ItemsKeysValuesMixin):
#     """Mapping s metodami .items(), .keys(), .values()"""
#     __slots__ = ()
#
# # 7. Inspectable — přidá Dir
# class Inspectable(DirMixin):
#     """Přidá podporu pro dir(obj)"""
#     __slots__ = ()
#
#
# # **Poznámka:** `Container` a `Iterable` jsou Python ABC protokoly — dobré názvy.
#
#
# __DOCT__ = """
# # GROUP: `collections/`
#
# > **Group purpose:**
# > The container protocols — everything needed to make an object behave like a Python
# > collection (list, dict, set, or any custom container). These dunders are called by
# > `len()`, `in` operator, `for` loops (when `__iter__` is absent), subscript access
# > (`obj[key]`), and mutation operations. Together they define whether your class is a
# > sequence, a mapping, a set-like structure, or all of the above.
# """