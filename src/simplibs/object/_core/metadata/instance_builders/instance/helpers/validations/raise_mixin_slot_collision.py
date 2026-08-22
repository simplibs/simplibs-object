from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slot_collision(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
    slot_name: str,
) -> None:
    """Raises an error when multiple mixins define the same __slots__ attribute name."""

    raise SimpleInitializationError(
        error_name="SLOT NAME COLLISION",
        label="mixin_slot_name_collision",
        expected="Unique __slots__ attribute names across all applied mixins",
        value=slot_name,
        problem=(
            f"Mixin '{mixin.__name__}' defines slot '{slot_name}', "
            f"which collides with an existing slot of the same name from another mixin "
            f"when building class_dict for '{cls.__name__}'."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            f"Rename slot '{slot_name}' in mixin '{mixin.__name__}' to prevent attribute collisions.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            f"        __slots__ = ('_{mixin.__name__.lower()}_{slot_name}',)",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slot_collision

## Purpose
Signals that two or more mixins in the flattened mixin tuple declare an identical 
`__slots__` attribute name during namespace dictionary compilation.

## Behavior
- Triggered when:
  - Iterating over mixin `__slots__` in `_build_instance_class_dict`
  - AND `slot in flat_slots` evaluates to `True`
- Raises `SimpleInitializationError` with a clear explanation of the colliding slot and mixin.

## Notes
- Consolidating all mixin slots into a single dynamic `__slots__` tuple on `class_dict` 
  prevents C-level slot layout errors in Python's dynamic type creation.
- Detecting duplicate slot names early at the framework level provides precise diagnostics 
  and prevents silent variable overwrites between mixins.
"""