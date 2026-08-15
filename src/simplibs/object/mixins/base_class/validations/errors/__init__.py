from .raise_mixin_slots_is_not_defined import raise_mixin_slots_is_not_defined
from .raise_mixin_slots_unsuport_type import raise_mixin_slots_unsuport_type
from .raise_mixin_slots_contain_unvalid_type import raise_mixin_slots_contain_unvalid_type
from .raise_mixin_slots_contains_forbidden_slot_names import raise_mixin_slots_contains_forbidden_slot_names
from .raise_mixin_dict_contains_forbidden_attributes import raise_mixin_dict_contains_forbidden_attributes
from .raise_mixin_flag_is_not_bool import raise_mixin_flag_is_not_bool
from .raise_mixin_only_types_invalid import raise_mixin_only_types_invalid
from .raise_mixin_init_mixins_missing_super_call import raise_mixin_init_mixins_missing_super_call

_DESIGN_NOTES = """
# Mixin Validation Error Package

## Purpose
Provides a complete suite of structured error factories used by the mixin
validation pipeline. Each function raises a `SimpleLogicError` with detailed,
developer-friendly diagnostics describing exactly why a mixin definition is
invalid.

These errors ensure that mixins remain safe, deterministic, and compatible with
the dynamic instance-building architecture of the Simple system.

## Internal Components Registry

| Component                                         | Type     | Description                                                             |
| :------------------------------------------------ | :------- | :---------------------------------------------------------------------- |
| `raise_mixin_slots_is_not_defined`                | Function | Ensures mixin defines its own `__slots__`.                              |
| `raise_mixin_slots_unsuport_type`                 | Function | Validates that `__slots__` is tuple or string.                          |
| `raise_mixin_slots_contain_unvalid_type`          | Function | Ensures all slot items are strings.                                     |
| `raise_mixin_slots_contains_forbidden_slot_names` | Function | Detects forbidden instance-level slot names.                            |
| `raise_mixin_dict_contains_forbidden_attributes`  | Function | Detects forbidden class-level attribute names.                          |
| `raise_mixin_flag_is_not_bool`                    | Function | Validates boolean compatibility flags.                                  |
| `raise_mixin_only_types_invalid`                  | Function | Validates structural correctness of `_only_types`.                      |
| `raise_mixin_init_mixins_missing_super_call`      | Function | Ensures overridden `init_mixins` calls `super().init_mixins()`.         |
"""
