from .raise_invalide_extend_instance_class_definition import raise_invalide_extend_instance_class_definition
from .raise_mixin_slot_collision import raise_mixin_slot_collision
from .raise_mixin_slot_collision_with_base_class import raise_mixin_slot_collision_with_base_class


_DESIGN_NOTES = """
# Instance Helper Validations Sub-Package

## Purpose
Provides specialized diagnostic and validation helpers used during dynamic instance class 
compilation and mixin resolution. Guarantees mixin compatibility and prevents attribute slot collisions.

## Internal Components Registry

| Component                                         | Type     | Description                                                                     |
| :------------------------------------------------ | :------- | :------------------------------------------------------------------------------ |
| `raise_invalide_extend_instance_class_definition` | Function | Raised when `__extend_instance_class__` is not a staticmethod or classmethod.   |
| `raise_mixin_slot_collision`                      | Function | Raised when multiple mixins declare overlapping `__slots__` attribute names.     |
| `raise_mixin_slot_collision_with_base_class`     | Function | Raised when a mixin declares a slot that shadows an existing base class slot.   |
"""