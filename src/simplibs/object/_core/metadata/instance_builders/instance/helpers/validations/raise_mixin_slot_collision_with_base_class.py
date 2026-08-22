from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slot_collision_with_base_class(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
    slot_name: str,
) -> None:
    """Raises an error when a mixin defines a slot that collides with a base class slot."""

    raise SimpleInitializationError(
        error_name="MIXIN BASE SLOT COLLISION",
        label="mixin_base_slot_collision",
        expected="Mixin slots distinct from base class __slots__ layout",
        value=slot_name,
        problem=(
            f"Mixin '{mixin.__name__}' defines slot '{slot_name}', "
            f"which shadows an existing slot from base class '{cls.__name__}' "
            f"when building class_dict."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            f"Rename or remove slot '{slot_name}' in mixin '{mixin.__name__}'.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            f"        __slots__ = ('_{mixin.__name__.lower()}_{slot_name}',)",
            f"Base class '{cls.__name__}' already owns this attribute slot layout.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slot_collision_with_base_class

## Purpose
Signals that a mixin declares a `__slots__` attribute name that already exists in the 
target base class hierarchy (`cls.__mro__`), preventing accidental descriptor shadowing.

## Behavior
- Triggered when:
  - Iterating over mixin `__slots__` in `_build_instance_class_dict`
  - AND `slot in base_slots` evaluates to `True`
- Raises `SimpleInitializationError` with diagnostic context identifying the shadowed slot.

## Notes
- Shadowing base class slots in dynamic subclassing can lead to undefined C-level memory 
  descriptor behavior and silent state corruption.
- Catching base slot collisions early guarantees structural memory integrity of the compiled instance.
"""