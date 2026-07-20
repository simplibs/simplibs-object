from typing import Any, TYPE_CHECKING
# Inners
from .helpers import (
    get_base_class,
    create_instance_class
)
from .helpers.validations import (
    validate_mixins,
    validate_hashing_for_immutable_value,
    validate_class_and_parameters,
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.instance import SimpleInstanceLike
    from .....protocols.alias_typings import MixinsTuple


def create_instance(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    *,
    as_atom: bool,
    mutable: bool = True,
    validate: bool = True
) -> Any:
    """Orchestrates the complete validation and compilation lifecycle of a new runtime instance."""

    # 1. Enforce class and parametrization constraints
    if validate:
        validate_class_and_parameters(cls, as_atom, mutable)

    # 2. Resolve structural layout mode (atomic vs. composite)
    is_atom = cls.meta.is_constant or as_atom

    # 3. Verify immutability safety and hashing contracts
    if not mutable:
        validate_hashing_for_immutable_value(cls)

    # 4. Dispatch and retrieve the appropriate structural base class
    base_class = get_base_class(cls, is_atom, mutable)

    # 5. Verify mixin safety and structural compatibility matrix
    if validate:
        validate_mixins(cls, mixins, is_atom, mutable)

    # 6. Dynamically compile the unified runtime instance type
    _instance_cls = create_instance_class(cls, mixins, base_class, is_atom, mutable)

    # 7. Apply mixin class transformations and dynamic extensions
    for mixin in mixins:
        if hasattr(mixin, "__extend_instance_class__"):
            _instance_cls = mixin.__extend_instance_class__(_instance_cls)

    # 8. Allocate clean raw memory slot for the new instance
    instance = object.__new__(_instance_cls)

    # 9. Execute pre-compiled instance initializers
    # Note: Both composite and atomic inners have mutability switches baked into their closures
    instance.__init__()

    # 10. Return the fully materialized operational instance matching the protocol
    instance: "SimpleInstanceLike"
    return instance


_DESIGN_NOTES = """
# create_instance

## Purpose
Acts as the central execution orchestrator of the instance factory subsystem. It coordinates metadata inspection, multi-level constraint checks, dynamic MRO class compilation, post-compilation mixin hooks, raw memory allocation, and reactive initialization.

## Architectural Design Decisions

### 1. Granular Linear Execution Pipeline
* The object assembly is broken down into independent, predictable stages (Validation -> Resolution -> Base Selection -> Class Compilation -> Extensions -> Memory Allocation -> Initialization).
* This clear linear progression keeps responsibilities separated and makes debugging easy. We can trace exactly whether an unexpected behavior happened during type compilation, mixin extension, or state initialization.

### 2. Bypassing Type Duplication with Class Extension Hooks (`__extend_instance_class__`)
* The factory introduces a two-phase class generation system: standard dynamic type assembly followed by optional mixin extension passes.
* If a mixin implements the `__extend_instance_class__` hook, it gets direct access to the compiled type before object allocation. This design pattern lets mixins inject low-level metaclass-like changes, register proxies, or wrap behaviors without forcing deep, nested multi-inheritance levels or complex metaclass combinations.

### 3. Decoupled Memory Allocation and Initialization (`object.__new__`)
* Instantiation uses low-level `object.__new__(_instance_cls)` followed by an explicit `instance.__init__()` call instead of high-level type invocation.
* This decoupling separates memory layout allocation from state setup. It ensures that the dynamically compiled closures (`create_atom_init` or `create_composite_init`) have complete control over tree bindings and slot layouts without standard python constructor interference.

### 4. Optional Validation Gateways for Performance Tuning
* The pipeline provides an optional `validate` toggle that controls the execution of structural verification checks.
* This architectural choice guarantees strict validation safety nets during development and configuration changes, while giving high-throughput serialization or hydration engines a way to skip redundant validations when loading trusted data sources.
"""