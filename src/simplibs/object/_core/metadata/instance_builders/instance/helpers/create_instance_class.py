from typing import TYPE_CHECKING
# Inners
from .validations import raise_mixin_slots_conflict_error
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.instance.core_classes import AtomInstanceProtocol, CompositeInstanceProtocol
    from .....protocols.alias_typings import MixinsTuple
    from .....protocols.instance import SimpleInstanceLike


def create_instance_class(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    base_class: "AtomInstanceProtocol | CompositeInstanceProtocol",
    is_atom: bool,
    mutable: bool,
) -> "SimpleInstanceLike":
    """Compiles a unified runtime instance class from mixins and the structural base."""

    # 1. Build MRO
    class_parents = (*mixins, base_class)
    class_name = f"{cls.meta.class_name}Instance"

    # 2. Build namespace
    class_dict = {
        "__slots__": (),
        "__is_constant__": is_atom,
        "__is_mutable__": mutable,
        "__mixins__": mixins,
    }

    # 3. Compile type (catch slot conflicts)
    try:
        # noinspection PyTypeChecker
        _instance_cls = type(class_name, class_parents, class_dict)
    except TypeError as error:
        raise_mixin_slots_conflict_error(cls, mixins, error)

    # 4. Standardize qualname
    _instance_cls: "SimpleInstanceLike"
    # noinspection PyUnboundLocalVariable
    _instance_cls.__qualname__ = class_name

    # 5. Return compiled class
    return _instance_cls


_DESIGN_NOTES = """
# create_instance_class

## Purpose
Builds the final runtime class for an instance by merging:
- the structural base class (atom/composite)
- all user‑provided mixins
- identity markers describing mutability and topology

## Behavior
1. Constructs the MRO as `(*mixins, base_class)`.
2. Defines an empty `__slots__` to avoid conflicts with base‑class slots.
3. Injects identity tokens:
   - `__is_constant__`
   - `__is_mutable__`
   - `__mixins__`
4. Compiles the class using `type()`.
5. Intercepts slot layout conflicts and routes them through
   `raise_mixin_slots_conflict_error`.
6. Normalizes `__qualname__` for debugging and introspection.

## Notes
- Mixins appear before the base class in the MRO, allowing them to override
  behavior while still supporting `super()`.
- Empty `__slots__` ensures compatibility with structural base classes that
  already define storage slots.
- This function returns a **class**, not an instance; instantiation happens later
  in `create_instance`.
"""