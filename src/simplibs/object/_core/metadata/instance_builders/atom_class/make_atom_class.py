from typing import TYPE_CHECKING
# Outers
from ....logic.property_builders import create_value_property
# Inners
from .InstanceBase import InstanceBase
from .helpers import create_atom_init, create_root_value_setter
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.instance.core_classes import AtomInstanceProtocol


def make_atom_class(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True,
) -> "AtomInstanceProtocol":
    """Creates a dynamically generated atomic instance class."""

    # 1. Build class name
    base_class_name = (
        f"{meta.class_name}AtomMutableBase"
        if mutable else
        f"{meta.class_name}AtomImmutableBase"
    )

    # 2. Define inheritance
    class_parents = (InstanceBase, meta.owner_class)

    # 3. Build class dictionary
    class_dict = {
        "_is_mutable": mutable,
        "__metadata__": meta,
        "__doc__": f"Atomic instance for {meta.class_name}",
        "__slots__": ("_value", "_owner", "_locked"),
        "__init__": create_atom_init(meta, base_class_name),
        "value": create_value_property(meta, mutable=mutable),
        "owner": property(lambda self: self._owner),
    }

    # 4. Add mutable-only setter
    if mutable:
        class_dict["_root_value_setter"] = create_root_value_setter(base_class_name)

    # 5. Create class
    # noinspection PyTypeChecker
    atom_class = type(
        base_class_name,
        class_parents,
        class_dict,
    )

    # 6. Return class
    atom_class: "AtomInstanceProtocol"
    return atom_class



_DESIGN_NOTES = """
# make_atom_class

## Purpose
Creates a lightweight atomic instance class using dynamic metaprogramming.
Atomic instances represent single-value nodes used both in constants and
composition structures.

## Behavior

### 1. Naming
Generates either a mutable or immutable variant based on the `mutable` flag.

### 2. Inheritance
Each atomic instance inherits:
- `InstanceBase` (identity, `_is_instance_class` flag, slots, metadata access)
- `meta.owner_class` (domain-specific behaviors)

### 3. Class dictionary
Defines:
- `_is_mutable` flag indicating mutability topology
- `__metadata__ = meta` mapping to ensure direct access to blueprint metadata
- slots (`_value`, `_owner`, `_locked`)
- constructor (`__init__`)
- value property
- owner property

### 4. Mutable-only setter
If mutable, injects `_root_value_setter` for reactive updates.

## Notes
- Inheriting `_is_instance_class` from `InstanceBase` prevents the metaclass from generating secondary metadata
  for compiled runtime classes (avoiding synthetic names like `*AtomMutableBase`).
- Direct assignment of `__metadata__` guarantees that `instance.meta` always resolves to
  the declarative blueprint specification.
- `class_dict` passed to `type(...)` only ever contains the members listed above — declarative
  attributes such as `_type`, `_default`, `_validate`, and `bool_or_raise_validate_error` are
  never placed there, so they are never present on the compiled class's own `__dict__` in the
  first place. They do, however, remain reachable through the MRO via `meta.owner_class`, since
  `type(...)` only controls the new class's own namespace, not what its parents already expose.
- This function is part of the public instance-building API and is used by both
  constant metadata and composition metadata.
"""
