from .to_dict import to_dict
from .from_dict import from_dict
from .from_dict_constants import from_dict_constants

_DESIGN_NOTES = """
# Serialization Utilities

## Purpose
Provides the core import/export utilities used by SerializationMixin. Handles
conversion between object instances and dictionary structures, supporting both
mutable and immutable operational modes.

## Internal Components Registry

| Component              | Type     | Description                                         |
| :--------------------- | :------- | :-------------------------------------------------- |
| `to_dict`              | Function | Serializes instance into a structured dictionary.   |
| `from_dict`            | Function | Reconstructs full instance state from a dictionary. |
| `from_dict_constants`  | Function | Updates only constant values from a partial dict.   |
"""
