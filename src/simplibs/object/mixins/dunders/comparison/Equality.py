from typing import TYPE_CHECKING, Any
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.comparison import EqualityProtocol


class Equality(SimpleMixin):
    """
    Equality and hashing for Simple instances.

    Equality (__eq__) is value-based:
    - If the other operand is a Simple instance of the same blueprint,
      their values are compared.
    - If the other operand is a raw value, it is compared directly.

    Hashing (__hash__) is driven by instance mutability:
    - For mutable instances (__is_mutable__ = True), identity-based hash
      (id(self)) is used, to guarantee stability even when the value
      changes.
    - For immutable instances (__is_mutable__ = False), value-based hash
      (hash(self.value)) is used, because the value is guaranteed to be
      immutable and hashable.

    This mixin is universal — it can be used for both mutable and
    immutable instances, since the hashing strategy is chosen dynamically
    based on the __is_mutable__ flag.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - EQ / HASH
    # ----------------------------------------

    def __eq__(
        self: "EqualityProtocol",
        other: Any
    ) -> bool:
        """
        Value-based equality.
        - If the other operand is a Simple instance of the same
          blueprint, their values are compared.
        - If the other operand is a raw value, it is compared directly.
        """
        # 1. Comparing two Simple instances
        if hasattr(other, "meta") and hasattr(other, "value"):
            if self.meta.blueprint_path == other.meta.blueprint_path:
                return self.value == other.value
            return False

        # 2. Comparing against a raw value
        return self.value == other

    def __hash__(
        self: "EqualityProtocol"
    ) -> int:
       """
       Returns a hash based on the instance's mutability.

       - For mutable instances (__is_mutable__ = True), returns a hash
         based on object identity (id(self)), to guarantee stability even
         when the value changes.

       - For immutable instances (__is_mutable__ = False), returns a
         value-based hash (hash(self.value)), because the value is
         guaranteed to be immutable and hashable.

       This method thus unifies hashing for both mutable and immutable
       mode within a single mixin.
       """
       return (
           id(self)
           if self.__is_mutable__ else
           hash(self.value)
       )


_DESIGN_NOTES = """
# Equality

## Purpose
Gives a Simple instance sensible `==` and `hash()` behavior, so instances
can be compared to each other, compared to raw values, and used as dict
keys or set members.

> For newcomers: Python requires that if two objects compare equal, their
> hashes must also match (otherwise `dict`/`set` break). This mixin's job
> is to keep that contract true for both mutable and immutable instances,
> which need very different hashing strategies.

## Compatibility
- No compatibility flags — works for atoms and composites, mutable and
  immutable alike. The logic branches internally on `__is_mutable__`
  instead of being restricted to one variant.

## Logic
`__eq__`:
- Comparing two Simple instances checks they share the same
  `meta.blueprint_path` (same definition) before comparing `.value` —
  two unrelated classes with an equal value are *not* equal.
- Comparing against a raw value compares `.value` directly, so
  `age == 20` works without unwrapping.

`__hash__` branches on `__is_mutable__`:
- **Mutable** → `id(self)` (identity hash). A mutable instance's value can
  change after being hashed; if the hash also changed, it would silently
  break in `dict`/`set`. Identity hash sidesteps that at the cost of
  `obj == obj_with_same_value` not implying `hash()` equality for two
  *different* mutable instances — which is expected, standard Python
  behavior for mutable objects.
- **Immutable** → `hash(self.value)`. The value can never change again,
  so it's safe and gives the intuitive result: two immutable instances
  with equal values hash equally too.

## Notes
- Defining `__eq__` without `__hash__` would make instances unhashable by
  default in Python — this mixin deliberately pairs both together.
- `blueprint_path` equality (not just type equality) means two instances
  built from structurally identical but differently-named blueprints are
  still treated as unequal.
"""
