from typing import Any, TYPE_CHECKING
# Outers
from ...constants import BASE_CLASS_NAMES
# Inners
from .helpers import get_base_class, create_instance_class
from .validations import (
    validate_class_is_not_base_class,
    validate_param_is_bool,
    validate_hashing_for_immutable_value,
    validate_mixins
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
    validate: bool = True,
) -> "SimpleInstanceLike":
    """Orchestrates the complete validation and compilation lifecycle of a new runtime instance."""

    # 1. Validate class identity and boolean parameters
    if validate:
        if cls.__name__ in BASE_CLASS_NAMES or not isinstance(as_atom, bool):
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

    # 5. Validate mixin compatibility
    if validate:
        validate_mixins(cls, mixins, is_atom, mutable)

    # 6. Compile unified runtime class
    _instance_cls = create_instance_class(cls, mixins, base_class, is_atom, mutable)

    # 7. Apply mixin extension hooks
    for mixin in mixins:
        if hasattr(mixin, "__extend_instance_class__"):
            _instance_cls = mixin.__extend_instance_class__(_instance_cls)

    # 8. Allocate raw memory for instance
    instance = object.__new__(_instance_cls)

    # 9. Run initializer (atomic/composite closures handle mutability internally)
    instance.__init__()

    # 10. Return fully materialized instance
    instance: "SimpleInstanceLike"
    return instance



_DESIGN_NOTES = """
# create_instance

## Purpose
Serves as the central orchestrator of the instance factory. Coordinates validation,
structural resolution, dynamic class compilation, mixin extension hooks, memory
allocation, and initialization into a single deterministic pipeline.

## Pipeline Overview
1. **Validation**
   Ensures class identity and boolean flags are correct. Prevents misuse of base
   classes and invalid configuration parameters.

2. **Topology Resolution**
   Determines whether the instance is atomic or composite based on metadata and
   the `as_atom` flag.

3. **Immutability Safety**
   Immutable instances must wrap hashable default values. This step enforces that
   contract early.

4. **Base Class Selection**
   Retrieves the correct structural class (atom/composite × mutable/immutable)
   from metadata.

5. **Mixin Compatibility**
   Validates mixin identity and structural constraints (`_constant_only`,
   `_composite_only`, `_mutable_only`, `_immutable_only`, `_only_types`).

6. **Dynamic Class Compilation**
   Builds the final runtime class using `type()`, merging mixins and the base
   class into a unified MRO.

7. **Mixin Extension Hooks**
   Mixins may optionally modify the compiled class via `__extend_instance_class__`.

8. **Memory Allocation**
   Uses `object.__new__` to allocate raw memory without invoking Python’s default
   constructor.

9. **Initialization**
   Executes the pre‑compiled initializer closure (atomic or composite), which
   handles mutability and structural setup.

10. **Return**
   Produces a fully operational instance implementing the `SimpleInstanceLike`
   protocol.

## Notes
- The pipeline is intentionally linear and granular, making debugging and tracing
  extremely predictable.
- Validation can be disabled for high‑performance hydration or deserialization
  scenarios.
- The separation of class compilation and instance allocation provides full
  control over memory layout and initialization semantics.
"""