from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .validations import verify_mixin_definition
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.base_class import SimpleMixinProtocol
    from ..._core.protocols.alias_typings import ValidTypes


class SimpleMixin:
    """
    Base class representing the structural interface for all mixins in the
    Simple system.

    Mixins may extend instance behavior, participate in initialization, and
    declare compatibility constraints that determine which instance types they
    may be applied to.
    """

    # ----------------------------------------
    # Declarative compatibility flags
    # ----------------------------------------

    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types: "ValidTypes" = UNSET

    # ----------------------------------------
    # Slot definition
    # ----------------------------------------

    __slots__ = ()

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    def init_mixins(
        self: "SimpleMixinProtocol",
    ) -> None:
        """
        Default initialization hook for mixins.

        Mixins overriding this method must call super().init_mixins() to
        preserve the initialization chain.
        """
        # noinspection PyUnresolvedReferences
        super().init_mixins()

    # ----------------------------------------
    # Class definition validator
    # ----------------------------------------

    def __init_subclass__(
        cls: "SimpleMixinProtocol",
        **kwargs,
    ) -> None:
        """
        Validates the structural correctness of the mixin definition whenever
        a new mixin subclass is created.
        """

        # 1. Run parent class initialization
        super().__init_subclass__(**kwargs)

        # 2. Validate mixin definition
        verify_mixin_definition(cls)


_DESIGN_NOTES = """
# SimpleMixin

## Purpose
`SimpleMixin` defines the foundational interface for all mixins in the Simple
system. Mixins extend instance behavior, participate in initialization, and
declare compatibility constraints that determine which instance types they may
be applied to.

This base class ensures that every mixin:

- defines its own memory layout (`__slots__`),
- participates correctly in the initialization chain,
- declares compatibility flags in a consistent manner,
- passes structural validation during class creation.

## Architectural reasoning
Mixins in the Simple system are dynamically merged into runtime-generated
instance classes. Because they directly modify instance behavior and memory
layout, they must follow strict structural rules.

`SimpleMixin` provides:

### 1. Declarative compatibility flags
These flags restrict mixin applicability based on instance type:

- `_constant_only`
- `_composite_only`
- `_mutable_only`
- `_immutable_only`
- `_only_types`

They allow mixins to express structural constraints without embedding logic
inside the instance builder.

### 2. Explicit slot definition
Mixins must define their own `__slots__` to ensure:

- predictable memory layout,
- safe merging with other mixins,
- prevention of accidental attribute creation.

### 3. Initialization hook
`init_mixins` allows mixins to participate in instance initialization.  
Overriding mixins must call `super().init_mixins()` to preserve the chain.

### 4. Automatic structural validation
`__init_subclass__` invokes `verify_mixin_definition`, ensuring that every mixin
subclass is validated at creation time. This prevents invalid mixins from ever
entering the system.

## Validation pipeline
The validator checks:

1. presence of `__slots__`,
2. slot type correctness,
3. slot item correctness,
4. forbidden slot names,
5. forbidden class attributes,
6. boolean restriction flags,
7. structural correctness of `_only_types`,
8. presence of `super().init_mixins()` in overridden hooks.

This guarantees that mixins are safe, deterministic, and compatible.

## Diagnostic value
Any structural mistake results in a structured `SimpleLogicError` with:

- clear explanation,
- actionable guidance,
- examples,
- contextual metadata.

This makes debugging mixin definitions fast and predictable.

## Notes
- `SimpleMixin` is not intended to be instantiated directly.
- All mixins in the Simple system must inherit from this class.
- The class is intentionally minimal; all heavy logic is delegated to the
  validator and mixin-specific implementations.
"""