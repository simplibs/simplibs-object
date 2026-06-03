from .Generic import GenericMixin
from .Copyable import CopyableMixin
from .Serializable import SerializableMixin
from .Persistent import PersistentMixin

__all__ = (
    "GenericMixin",
    "CopyableMixin",
    "SerializableMixin",
    "PersistentMixin",
)



# # lifecycle/__init__.py
#
# # 1. Copyable — mělká + hluboká kopie
# class Copyable(CopyMixin, DeepcopyMixin):
#     """Podporuje copy() a deepcopy()"""
#     __slots__ = ()
#
# # 2. Serializable — pickle protokol
# class Serializable(GetstateMixin, SetstateMixin, ReduceMixin):
#     """Podporuje pickle (getstate, setstate, reduce)"""
#     __slots__ = ()
#
# # 3. Generic — generics support
# class Generic(ClassGetitemMixin):
#     """Podporuje MyClass[int] syntax"""
#     __slots__ = ()
#
# # 4. Persistent — Copyable + Serializable
# class Persistent(CopyMixin, DeepcopyMixin, GetstateMixin, SetstateMixin, ReduceMixin):
#     """Plná podpora kopírování i serializace"""
#     __slots__ = ()
#
#
# __DOCT__ = """
# # GROUP: `lifecycle/`
#
# > **Group purpose:**
# > Everything related to *when* and *how* an object comes into being, exists, gets copied,
# > and eventually disappears. This group covers the full lifespan of a Python object —
# > from class-level hooks that fire when a class is *defined*, through construction and
# > initialization of instances, all the way to destruction and serialization.
# > If you think of an object as a living entity, this group is its birth, life and death certificate.
# """