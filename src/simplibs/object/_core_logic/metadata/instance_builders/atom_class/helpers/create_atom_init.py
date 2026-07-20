from typing import TYPE_CHECKING
from collections.abc import Callable
from simplibs.sentinels import UNSET
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance import SimpleInstanceLike


def create_atom_init(
    meta: "SimpleMetadataLike",
    base_class_name: str
) -> Callable:
    """Generates a specialized factory initialization method closure for atomic instances.

    Binds core metadata constraints, defaults, and architectural invariants directly
    into the runtime execution footprint of the generated function object.
    """

    # 1. Define the internal constructor routine closure logic
    def __init__(
        self: "SimpleInstanceLike"
    ) -> None:

        # Materialize the initial instance value using the metadata default factory schema
        self._value = meta.default

        # Initialize the structural composition parent link to the architectural UNSET sentinel
        self._owner = UNSET

        # Initialize the low-level value modification barrier state lock flag
        self._locked = False

        # Trigger the dynamic structural mixin injection pipeline hook anchor
        self.init_mixins()

    # 2. Re-bind dynamic reflection attributes to guarantee transparent stack traces
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    # 3. Yield the constructed execution constructor closure method
    return __init__


_DESIGN_NOTES = """
# create_atom_init

## Purpose
Acts as a low-level structural factory function that yields encapsulated `__init__` constructor methods for dynamically built atomic classes (`type(...)`). It isolates class-generation mechanics, preventing metadata lookup overhead during subsequent runtime object instantiations.

## Architectural Design Decisions

### 1. Closure-Bound Scope Isolation & Optimization
* Instead of fetching `meta.default` inside a generic boilerplate method via standard runtime attribute resolution, the utility uses a Python closure layout. 
* This captures the specific `meta` payload reference directly inside the local namespace cell scope of the generated `__init__` object. This eliminates redundant dynamic attribute traversal down the instance chain during performance-critical allocation loops.

### 2. Invariant Initialization Matrix
* **`self._value`**: Seeded directly from the metadata schema definition to establish the baseline payload contract immediately upon allocation.
* **`self._owner = UNSET`**: Intentionally decouples the instance from any composition structure at birth. By avoiding a `None` default, the engine distinguishes between an element explicitly unlinked from a tree versus an uninitialized element state via the `UNSET` sentinel.
* **`self._locked = False`**: Establishes the mutable initialization window before state locking operations freeze down the internal state properties.

### 3. Reflection Alignment and Debuggability
* Manually overriding `__name__` and `__qualname__` ensures that standard Python inspection frameworks, profiling engines, and stack tracers read the generated method as a native member of the synthesized target class (`e.g., MyClassAtomMutableBase.__init__`) rather than an anonymous nested block function.
"""