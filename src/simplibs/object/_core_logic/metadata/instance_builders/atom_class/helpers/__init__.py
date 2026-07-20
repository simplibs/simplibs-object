from .create_atom_init import create_atom_init
from .create_root_value_setter import create_root_value_setter

_DESIGN_NOTES = """
# Atomic Class Builders Helpers Sub-Package

## Purpose
Houses specialized low-level functional generators designed to inject core initialization and state management hooks into dynamic atomic runtime classes.

## Internal Components Registry

| Component                  | Type     | Description                                                                          |
| :------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `create_atom_init`         | Function | Generates the optimized `__init__` constructor method closure for atomic instances.  |
| `create_root_value_setter` | Function | Generates the unified internal `_root_value_setter` method for atomic value tracking.|
"""