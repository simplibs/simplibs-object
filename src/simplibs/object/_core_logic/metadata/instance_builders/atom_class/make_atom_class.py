from typing import TYPE_CHECKING
# Outers
from ....properties import create_value_property
# Inners
from .InstanceBase import InstanceBase
from .helpers import create_atom_init, create_root_value_setter
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import AtomInstanceProtocol


def make_atom_class(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True
) -> "AtomInstanceProtocol":
    """Metaprogramming class factory that dynamically constructs atomic instance types.

    Assembles class dictionaries, defines inheritance hierarchies, configures static slots,
    and binds property behaviors tailored to the provided structural metadata rules.
    """

    # 1. Define the synthesized target class nomenclature configuration
    base_class_name = (
        f"{meta.class_name}AtomMutableBase"
        if mutable else
        f"{meta.class_name}AtomImmutableBase"
    )

    # 2. Define structural class lineage boundaries (inheritance parent matrix)
    class_parents = (InstanceBase, meta.owner_class,)

    # 3. Assemble target class dictionary layout specifications
    class_dict = {
        "__doc__": f"Atomic instance data target object for {meta.class_name}",
        "__slots__": ("_value", "_owner", "_locked"),
        "__init__": create_atom_init(meta, base_class_name),
        "value": create_value_property(meta, mutable=mutable),
        "owner": property(lambda self: self._owner, doc="Reference linking back to the parent composition node layer.")
    }

    # 4. Conditionally inject mutable-only logic mutators
    if mutable:
        class_dict["_root_value_setter"] = create_root_value_setter(meta, base_class_name)

    # 5. Execute low-level type metaclass constructor allocation
    # noinspection PyTypeChecker
    atom_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 6. Clean declarative configuration artifacts to prevent downstream namespace pollution
    for name in ("_type", "_default", "_validate", "bool_or_raise_validate_error"):
        if name in atom_class.__dict__:
            delattr(atom_class, name)

    # 7. Yield the fully compiled runtime type descriptor object
    atom_class: "AtomInstanceProtocol"
    return atom_class


_DESIGN_NOTES = """
# make_atom_class

## Purpose
Acts as a dynamic metaprogramming factory responsible for generating specialized, lightweight class definitions (`type(...)`) representing Atomic components. It compiles static schemas into concrete executable Python types at system initialization, avoiding dynamic parsing overhead at runtime instantiation loops.

## Architectural Design Decisions

### 1. Metaprogramming Paradigm & Dynamic Type Building
* The usage of the three-argument form of `type(name, bases, dict)` allows the engine to isolate configuration blueprints from real-world memory objects. By decoupling class synthesis from static source code declarations, the system can seamlessly morph behaviors based on whether the entity is marked `mutable` or `immutable`.
* Dynamic naming conventions (`*AtomMutableBase` vs `*AtomImmutableBase`) guarantee that stack traces, system logs, and debuggers can explicitly isolate object state anomalies down to the strict mutant tracking layer.

### 2. Multi-Inheritance Structure Integration (`class_parents`)
* By combining `InstanceBase` with `meta.owner_class`, the newly allocated type inherits global identity invariants alongside specific behaviors declared on the user-defined domain model class. 
* To maintain strict performance guidelines, `InstanceBase` is injected first to anchor slot structures and baseline representations before executing downstream method resolution paths.

### 3. Namespace Sanitization & Memory Integrity Guarding
* **Slot Rigidity**: Hardcoding `__slots__` inside the class dictionary cuts out structural dictionary allocations. It caps the memory footprint of every atomic instance to a highly predictable layout containing exactly three references (`_value`, `_owner`, `_locked`).
* **Declarative Scrubbing (`delattr`)**: Removing blueprint extraction variables (`_type`, `_default`, etc.) from the compiled class dictionary ensures that downstream runtime instances cannot accidentally resolve or modify definition-level parameters through fallback lookups. This prevents state contamination and enforces an immutable separation between schema specs and operational instances.
"""