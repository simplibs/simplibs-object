from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from ._meta import SimpleMixinMeta
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.base_class import SimpleMixinProtocol
    from ..._core.protocols.alias_typings import ValidTypes


class SimpleMixin(metaclass=SimpleMixinMeta):
    """Base class representing the structural interface for all mixins in the Simple system.

    Mixins may extend instance behavior, participate in initialization, and declare
    compatibility constraints that determine which instance types they may be applied to.
    """

    # ----------------------------------------
    # Declarative compatibility flags
    # ----------------------------------------

    _constant_only: bool = False
    _composite_only: bool = False
    _mutable_only: bool = False
    _immutable_only: bool = False
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
        """Default initialization hook for mixins.

        Mixins overriding this method should only initialize their own internal
        slots and state. Do NOT call super().init_mixins() as mixin hook chaining
        is orchestrated by the instance compilation engine.
        """
        pass


_DESIGN_NOTES = """
# SimpleMixin

## Purpose
`SimpleMixin` defines the foundational interface for all mixins in the Simple
system. Mixins extend instance behavior, participate in initialization, and
declare compatibility constraints that determine which instance types they may
be applied to.

This base class ensures that every mixin:

- defines its own memory layout (`__slots__`),
- declares an isolated initialization hook (`init_mixins`),
- declares compatibility flags in a consistent manner,
- passes structural validation during class definition via `SimpleMixinMeta`.

## Architectural reasoning
Mixins in the Simple system are dynamically merged into runtime-generated
instance classes via dictionary synthesis rather than Python's MRO. Because
they directly modify instance behavior and memory layout, they must follow
strict structural rules.

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

### 3. Isolated initialization hook
`init_mixins` allows mixins to initialize their own internal slots and state.  
Because the instance builder orchestrates and composes all mixin hooks iteratively,
overriding mixins MUST NOT call `super().init_mixins()`.

### 4. Metaclass structural validation
`SimpleMixinMeta` triggers `verify_mixin_definition` upon mixin class creation.
This guarantees fail-fast validation and prevents structurally invalid mixins
from entering the runtime engine.

## Diagnostic value
Any structural mistake results in a structured `SimpleRuntimeError` with:

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