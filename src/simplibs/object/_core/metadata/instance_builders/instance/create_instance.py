from typing import TYPE_CHECKING
# Outers
from ...constants import BASE_CLASS_NAMES
# Inners
from .helpers.create_instance_class import create_instance_class
from .helpers.get_base_class import get_base_class
from .validations import (
    validate_class_is_not_base_class,
    validate_param_is_bool,
    validate_hashing_for_immutable_value,
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike
    from ....protocols.instance import SimpleInstanceLike
    from ....protocols.alias_typings import MixinsTuple


def create_instance(
    cls: "SimpleClassLike",
    *,
    mixins: "MixinsTuple",
    as_atom: bool,
    mutable: bool = True,
) -> "SimpleInstanceLike":
    """Orchestrates the complete validation and compilation lifecycle of a new runtime instance."""

    # 1. Validate class identity and boolean parameters
    if (
        cls.__name__ in BASE_CLASS_NAMES
        or not isinstance(as_atom, bool)
        or not isinstance(mutable, bool)
    ):
        validate_class_is_not_base_class(cls)
        validate_param_is_bool(as_atom)
        validate_param_is_bool(mutable)

    # 2. Resolve structural mode (atomic vs composite)
    is_atom = cls.meta.is_constant or as_atom

    # 3. Validate immutability hashing contract
    if not mutable:
        validate_hashing_for_immutable_value(cls)

    # 4. Select structural base class
    base_class = get_base_class(cls, is_atom, mutable)

    # 5. Compile unified instance class (resolves mixins, namespace, slots, and extension hooks)
    # noinspection PyTypeChecker
    _instance_cls = create_instance_class(cls, mixins, base_class, is_atom, mutable)

    # 6. Allocate raw memory for instance
    instance = object.__new__(_instance_cls)

    # 7. Run initializer (atomic/composite closures handle mutability internally)
    instance.__init__()

    # 8. Return fully materialized instance
    return instance


_DESIGN_NOTES = """
# create_instance

## Purpose
Serves as the high-level orchestrator for constructing runtime instances in the Simple system.
It coordinates parameter validation, structural topology resolution, dynamic class compilation,
memory allocation, and instance initialization in a strict, deterministic sequence.

## Lifecycle Pipeline
1. **Identity & Parameter Guard**
   Guards against passing abstract base system classes as blueprint sources and validates
   that structural parameters (`as_atom`, `mutable`) are boolean primitives.

2. **Structural Topology Resolution (`is_atom`)**
   Evaluates whether the instance behaves as a single value container (atom) or a composite structure.
   Constants automatically force atomic topology regardless of `as_atom`.

3. **Immutability Contract Validation**
   Ensures that immutable targets wrap hashable default values before class allocation begins.

4. **Base Class Selection (`get_base_class`)**
   Delegates to `get_base_class` to fetch the cached structural core class 
   (atom/composite × mutable/immutable).

5. **Class Compilation (`create_instance_class`)**
   Triggers namespace construction, mixin flattening/injection, slot validation, and 
   metaprogramming extension hooks to produce a clean runtime class `_instance_cls`.

6. **Raw Memory Allocation (`object.__new__`)**
   Allocates memory directly on the compiled runtime class without triggering parent `__init__`
   constructors prematurely.

7. **Initialization (`instance.__init__`)**
   Executes the compiled initializer closure which sets up reactive storage, internal state,
   and chained `init_mixins` hooks.

8. **Materialization**
   Returns a fully initialized instance conforming to `SimpleInstanceLike`.

## Architectural Notes
- **Decoupled Validation**: Mixin resolution and validation are deferred to `create_instance_class` 
  and its helper pipeline (`_resolve_flat_mixins`), keeping `create_instance` lightweight and focused.
- **Two-Phase Construction**: Separating class compilation (`create_instance_class`) from instance 
  allocation (`object.__new__`) ensures that dynamic class generation happens once per execution path,
  leaving memory layout clean and deterministic.
"""