from typing import TYPE_CHECKING
# Inners
from .validations import raise_mixin_slots_conflict_error
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.classes import SimpleClassLike
    from ......protocols.instance.core_classes import AtomInstanceProtocol, CompositeInstanceProtocol
    from ......protocols.alias_typings import MixinsTuple
    from ......protocols.instance import SimpleInstanceLike


def create_instance_class(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    base_class: "AtomInstanceProtocol | CompositeInstanceProtocol",
    is_atom: bool,
    mutable: bool
) -> "SimpleInstanceLike":
    """Compiles a new runtime instance class architecture.

    - Combines the selected user/system mixins and the pre-compiled structural
      `base_class` into a unified Method Resolution Order (MRO).
    - Dynamically synthesizes the type structure via `type()`, injecting crucial
      technical identity descriptors:
        * __slots__        – defined as empty to grant mixins complete control over slots allocation
        * __is_constant__  – boolean flag pinning the atom/composite classification mode
        * __is_mutable__   – boolean flag pinning the mutability behavior profile
        * __mixins__       – a tuple record containing all attached mixin dependencies
    - Catches and routes layout definition slot conflicts between mixins and the structural base.
    - Explicitly overrides `__qualname__` for transparent string representation and debugging.
    - Returns the compiled runtime class type (not an object instance).
    """

    # 1. Gather structural payload records for dynamic type assembly
    class_parents = (*mixins, base_class)
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = {
        "__slots__": (),
        "__is_constant__": is_atom,
        "__is_mutable__": mutable,
        "__mixins__": mixins
    }

    # 2. Synthesize the functional runtime class type (intercepting slot configuration faults)
    try:
        # noinspection PyTypeChecker
        _instance_cls = type(
            class_name,
            class_parents,
            class_dict
        )
    except TypeError as error:
        raise_mixin_slots_conflict_error(cls, mixins, error)

    # 3. Standardize class identification path references
    # noinspection PyUnboundLocalVariable
    _instance_cls.__qualname__ = class_name

    # 4. Return the fully materialized type object matching the protocol
    _instance_cls: "SimpleInstanceLike"
    # noinspection PyUnboundLocalVariable
    return _instance_cls


_DESIGN_NOTES = """
# create_instance_class

## Purpose
Acts as the dynamic final type-compiler for individual node instances. It merges the core compiled structural bases (Atoms/Composites) with external mixin matrices, creating a customized, high-performance runtime class blueprint.

## Architectural Design Decisions

### 1. Dynamic MRO Injection Framework
* By packing `(*mixins, base_class)` into the `bases` tuple of `type()`, this factory builds a precise Method Resolution Order (MRO). 
* Mixins are positioned before the core structural `base_class`. This enables them to intercept standard method dispatches (e.g., overriding formatting or representation hooks) while maintaining direct access to underlying state variables through `super()`.

### 2. Empty Local Slots Allocation Policy (`__slots__ = ()`)
* The dynamically compiled instance type explicitly defines an empty `__slots__ = ()` declaration.
* In Python, a subclass cannot declare non-empty slots if it inherits from a base that has them, unless the layouts match perfectly. Since the structural `base_class` already defines data storage slots (like private pointers), setting empty slots here permits the MRO to compile smoothly while passing structural data access down to the base layout levels.

### 3. Slot Conflict Interception and Error Routing
* Merging multiple mixins into a dynamic `type()` wrapper often triggers Python C-level layout conflicts (e.g., multiple bases declaring non-empty slots or layout footprints).
* Wrapping compilation inside a `try/except TypeError` block catches these low-level errors at runtime. It routes raw C-level messages into `raise_mixin_slots_conflict_error` to provide clear, actionable feedback regarding overlapping data layouts.

### 4. Metadata Token Injection
* The compiler bakes identity tokens (`__is_constant__`, `__is_mutable__`, `__mixins__`) directly into the class dictionary namespace.
* Attaching these markers to the type level allows inspection systems, validation pipelines, and serialization runners to quickly determine instance behavior properties without executing slow class property lookups or instantiating dummy instances.
"""