from typing import TYPE_CHECKING, Callable
from simplibs.sentinels import UNSET
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance import SimpleInstanceLike


def create_atom_init(
    meta: "SimpleMetadataLike",
    base_class_name: str,
) -> Callable:
    """Creates the __init__ method for atomic instances."""

    # 1. Constructor closure
    def __init__(self: "SimpleInstanceLike") -> None:
        self._value = meta.default
        self._owner = UNSET
        self._locked = False
        self.init_mixins()

    # 2. Reflection alignment
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    # 3. Return constructor
    return __init__



_DESIGN_NOTES = """
# create_atom_init

## Purpose
Generates the `__init__` method for dynamically created atomic instance classes.
The method is implemented as a closure so that metadata values (`meta.default`)
are captured efficiently without repeated lookups.

## Behavior
1. Initializes:
   - `_value` from metadata default,
   - `_owner` as UNSET,
   - `_locked` as False.
2. Calls `init_mixins()` to allow dynamic extensions.
3. Rebinds `__name__` and `__qualname__` so stack traces and introspection
   show the method as a native member of the generated class.

## Notes
This function is internal to the instance-building pipeline and is not part of
the public API.
"""