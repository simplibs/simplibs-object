# Inners
from ._verify_mixin_definition import _verify_mixin_definition


class SimpleMixinMeta(type):
    """Metaclass for all mixins in the Simple system.

    Provides runtime type resolution via `isinstance` checks against flattened
    `__mixins__` tuples and executes static definition validation upon class creation.
    """

    def __init__(cls, name: str, bases: tuple[type, ...], dct: dict[str, object], **kwargs) -> None:
        super().__init__(name, bases, dct, **kwargs)

        # Run structural verification for all derived mixin classes (skip root SimpleMixin)
        if bases:
            _verify_mixin_definition(cls)

    def __instancecheck__(cls, instance: object) -> bool:
        """Intercepts `isinstance(obj, MyMixin)` calls to inspect the internal

        `__mixins__` tuple attached to compiled instance classes.
        """
        # 1. Standard MRO instance check (covers direct mixin instances if any exist)
        if super().__instancecheck__(instance):
            return True

        # 2. Inspect dynamically attached mixin registry on runtime instance classes
        mixins = getattr(instance, "__mixins__", ())

        # Returns True if this mixin class or any of its subclasses are registered
        return any(issubclass(m, cls) for m in mixins)


_DESIGN_NOTES = """
# SimpleMixinMeta

## Purpose
`SimpleMixinMeta` serves as the foundational metaclass for all mixin definitions in the Simple framework.
It addresses two architectural requirements in dynamic mixin systems:
1. Enforces strict definition-time structural validation on all mixin subclasses.
2. Bridges runtime identity checks (`isinstance()`) for dynamic instances that do not include mixins in their MRO.

## Core Mechanisms

### 1. Definition-Time Validation (`__init__`)
When a mixin class is declared, `SimpleMixinMeta.__init__` triggers `verify_mixin_definition(cls)`.
- **Root Skipping (`if bases:`)**: The root `SimpleMixin` class has an empty `bases` tuple and is excluded 
  from validation, allowing clean base-level defaults without triggering self-validation errors.
- **Fail-Fast Subclassing**: Any derived mixin is immediately validated against slot declarations, forbidden 
  namespace identifiers, flag typings, and hook signatures before it can be used anywhere in the codebase.

### 2. Flat Mixin Registry Resolution (`__instancecheck__`)
Because runtime instance classes compile mixin methods directly into `class_dict` rather than placing 
mixins into Python's MRO, standard Python `isinstance(instance, TargetMixin)` would normally return `False`.
- `__instancecheck__` intercepts the check and inspects `instance.__mixins__` (the flat registry tuple).
- Returns `True` if `TargetMixin` or any of its subclasses are present in `__mixins__`.
- Preserves standard polymorphic semantics and duck-typing without incurring MRO multi-inheritance layout overhead.
"""