from .HISTORY import HISTORY
from .OWNER_CLASS import OWNER_CLASS
from .STEPPER import STEPPER
from .VALUE import VALUE

_DESIGN_NOTES = """
# Internal Attribute Name Tokens

## Purpose
Provides a collection of atomic, immutable string tokens used as canonical
attribute identifiers throughout the Simple mixin and object system. Each
constant represents a single internal attribute name and acts as the sole
source of truth for that identifier.

## Internal Components Registry

| Component      | Type     | Description                                             |
| :------------- | :------- | :------------------------------------------------------ |
| `HISTORY`      | Constant | Internal attribute name for history tracking.           |
| `OWNER_CLASS`  | Constant | Internal attribute name for owner class reference.      |
| `STEPPER`      | Constant | Internal attribute name for stepper logic.              |
| `VALUE`        | Constant | Internal attribute name for value storage.              |

## Notes
These constants prevent accidental typos, shadowing, and inconsistent naming
across mixins and internal utilities. Each is intentionally isolated in its own
module to maintain a clear mental map of the system’s internal vocabulary.
"""
