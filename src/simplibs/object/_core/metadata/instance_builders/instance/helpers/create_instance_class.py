from typing import TYPE_CHECKING
# Inners
from ._build_instance_class_dict import _build_instance_class_dict
from ._extend_instance_class import _extend_instance_class
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.alias_typings import MixinsTuple
    from .....protocols.instance import SimpleInstanceLike


def create_instance_class(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    base_class: type,
    is_atom: bool,
    mutable: bool,
) -> "SimpleInstanceLike":
    """Compiles a unified runtime instance class by synthesizing namespace, mixins, and base class."""

    # 1. Define arguments for dynamic type creation
    class_name = f"{cls.meta.class_name}Instance"
    class_parents = (base_class,)
    class_dict = _build_instance_class_dict(cls, mixins, is_atom, mutable)

    # 2. Compile dynamic instance class
    _instance_cls = type(class_name, class_parents, class_dict)

    # 3. Standardize qualname for introspection
    _instance_cls.__qualname__ = class_name

    # 4. Apply metaprogramming extension hooks in-place
    _instance_cls: "SimpleInstanceLike"
    _extend_instance_class(class_dict["__mixins__"], _instance_cls)

    # 5. Return compiled instance class
    return _instance_cls


_DESIGN_NOTES = """
# create_instance_class

## Purpose
Compiles the dynamic runtime class (`*_Instance`) for a given blueprint and mixin set.
Rather than placing mixins directly into Python's MRO (`class_parents`), this function 
implements a **Namespace Injection Pattern**: mixins are flattened, validated, and merged
into `class_dict`, leaving `base_class` as the sole parent in MRO.

## Compilation Steps
1. **Namespace Assembly (`_build_instance_class_dict`)**
   Flattens the MRO tree of all provided mixins, validates individual mixin compatibility, 
   checks for slot collision, merges attributes/methods, and chains `init_mixins` hooks.
   Also attaches `__mixins__` (tuple of flattened mixin classes) to `class_dict`.

2. **Class Creation (`type()`)**
   Constructs the new type with single inheritance `(base_class,)`. This eliminates C-level 
   slot arrangement conflicts in Python's MRO while preserving clean behavior.

3. **Qualname Standardization**
   Sets `__qualname__` to match `class_name` for clean stack traces, help(), and debugging.

4. **In-Place Metaprogramming Extension (`_extend_instance_class`)**
   Executes static `__extend_instance_class__` hooks present on flattened mixins. This allows 
   advanced mixins (e.g., `InnersProperty`, `Equalizer`, `ImmutableWithInners`) to dynamically 
   attach generated properties or setters directly onto `_instance_cls`.

## Why Single Parent in MRO `(base_class,)`?
- **No Slot Layout Conflicts**: Mixins define their own slots. In standard Python multiple inheritance,
  combining multiple classes with non-empty `__slots__` raises a `TypeError`. Injecting mixin slots 
  and attributes directly into `class_dict` bypasses MRO slot limitations completely.
- **Explicit Ancestry Tracking**: Mixin membership is tracked explicitly via `class_dict["__mixins__"]`
  and validated at runtime via `SimpleMixinMeta.__instancecheck__`, making `isinstance(obj, Mixin)`
  work seamlessly without MRO complexity.
- **Predictable Method Resolution**: Attribute collisions are caught and resolved predictably during
  `class_dict` assembly rather than relying on complex MRO ordering.
"""