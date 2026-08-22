from typing import TYPE_CHECKING, Any
# Inners
from ._resolve_flat_mixins import _resolve_flat_mixins
from ._build_combined_init_mixins import _build_combined_init_mixins
from .validations import raise_mixin_slot_collision, raise_mixin_slot_collision_with_base_class
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.alias_typings import MixinsTuple


# Namespace keys excluded during dynamic class_dict synthesis
IGNORED_DICT_KEYS = {
    "__dict__",                  # Instance attribute dictionary descriptor (omitted for slot-based layout)
    "__weakref__",               # Weak reference support descriptor (omitted for slot-based layout)
    "__slots__",                 # Raw slot declarations (processed and aggregated separately into target slots)
    "__doc__",                   # Mixin docstring (prevents shadowing target class documentation)
    "__module__",                # Mixin source module name (prevents corrupting target class module path)
    "__init_subclass__",         # Subclass initialization hook (irrelevant for dynamic runtime instance types)
    "__extend_instance_class__", # Metaprogramming hook executed separately in-place after class compilation
}


def _build_instance_class_dict(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    is_atom: bool,
    mutable: bool,
) -> dict:
    """Builds the complete class_dict for compiling a new dynamic instance class."""

    # 1. Flatten and validate all mixin hierarchy nodes
    all_unique_mixins = _resolve_flat_mixins(cls, mixins, is_atom, mutable)

    # 2. Initialize base namespace dictionary
    class_dict: dict[str, Any] = {
        "__is_constant__": is_atom,
        "__is_mutable__": mutable,
        "__mixins__": all_unique_mixins,
    }

    # 3. Prepare collection containers and extract base class slots
    init_mixins = []
    mixin_slots = {}
    class_slots = {
        slot
        for base in cls.__mro__
        for slot in getattr(base, "__slots__", ())
    }

    # 4. Traverse mixins in reverse order for standard override precedence
    for mixin in reversed(all_unique_mixins):

        # 4.1 Process mixin slots & check for name collisions
        mixin_declared_slots = getattr(mixin, "__slots__", ())
        for slot in mixin_declared_slots:

            # 4.1.1 Check collision against base class slots
            if slot in class_slots:
                raise_mixin_slot_collision_with_base_class(cls, mixin, slot)

            # 4.1.2 Check collision against previously registered mixin slots
            if slot in mixin_slots:
                raise_mixin_slot_collision(cls, mixin, slot)

            # 4.1.3 Register unique slot name
            mixin_slots[slot] = None

        # 4.2 Extract namespace attributes
        for key, value in mixin.__dict__.items():

            # 4.2.1 Skip internal framework keys, metadata, and slot descriptors
            if key in IGNORED_DICT_KEYS or key in mixin_declared_slots:
                continue

            # 4.2.2 Isolate mixin initialization hooks
            if key == "init_mixins":
                init_mixins.append(value)

            # 4.2.3 Inject attribute or method into target class namespace
            else:
                class_dict[key] = value

    # 5. Attach unified initialization hook if mixin inits were declared
    if init_mixins:
        class_dict["init_mixins"] = _build_combined_init_mixins(init_mixins)

    # 6. Consolidate non-conflicting slots tuple
    class_dict["__slots__"] = tuple(mixin_slots.keys())

    # 7. Return fully synthesized namespace dictionary
    return class_dict


_DESIGN_NOTES = """
# _build_instance_class_dict

## Purpose
Constructs the target `class_dict` used by `type()` during dynamic runtime class compilation. 
Aggregates slots, methods, attributes, and markers from all flattened mixins into a single namespace.

## Pipeline & Logic
1. **Mixin Flattening**
   Delegates to `_resolve_flat_mixins` to get a deduplicated list of all mixin classes.

2. **Reversed Extraction (`reversed(all_unique_mixins)`)**
   Iterates through mixins in reverse order so that primary (earlier) mixins in the user-provided 
   tuple take precedence and cleanly overwrite attributes defined by secondary (later) mixins.

3. **Slot Name Collision Prevention**
   Traverses `__slots__` of all mixins and collects them into `mixin_slots`. If a slot collides with 
   the base class (`raise_mixin_slot_collision_with_base_class`) or another mixin (`raise_mixin_slot_collision`),
   an initialization exception is raised immediately.

4. **Namespace Filtering (`IGNORED_DICT_KEYS` & Slot Descriptors)**
   Filters out class boilerplate (`__dict__`, `__doc__`, `__module__`, `__weakref__`), metaprogramming hooks 
   (`__extend_instance_class__`), and mixin-declared slot descriptors to prevent namespace pollution and 
   `ValueError` collisions with `__slots__`.

5. **Init Hook Chaining**
   Isolates `init_mixins` functions from all mixins and chains them into a single executable 
   closure via `_build_combined_init_mixins`.

## Architectural Notes
- **Clean Slot Layout**: Consolidating all mixin slots into a single `__slots__` tuple on `class_dict` 
  guarantees C-level slot compatibility in Python without encountering multi-parent slot conflicts.
"""