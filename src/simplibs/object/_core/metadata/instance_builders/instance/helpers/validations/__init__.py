from .raise_mixin_slots_conflict_error import raise_mixin_slots_conflict_error


_DESIGN_NOTES = """
# Instance Helper Validations Sub-Package

## Purpose
Provides structured validation helpers used during instance class compilation.
Ensures mixin compatibility and prevents slot layout conflicts.

## Internal Components Registry

| Component                        | Type     | Description                                      |
| :------------------------------- | :------- | :------------------------------------------------ |
| `raise_mixin_slots_conflict_error` | Function | Raised when mixins define incompatible `__slots__` layouts. |
"""
