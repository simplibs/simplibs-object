from typing import TYPE_CHECKING, Union
from simplibs.sentinels import UNSET
# Outers
from ..._commons.constants import FORBIDDEN_NAMES, RESTRICTION_FLAGS
# Inners
from .errors import (
    raise_mixin_slots_is_not_defined,
    raise_mixin_slots_unsuport_type,
    raise_mixin_slots_contains_forbidden_slot_names,
    raise_mixin_dict_contains_forbidden_attributes,
    raise_mixin_slots_contain_unvalid_type,
    raise_mixin_init_mixins_missing_super_call,
    raise_mixin_flag_is_not_bool,
    raise_mixin_only_types_invalid,
)
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.base_class import SimpleMixinProtocol


def verify_mixin_definition(
    cls: "SimpleMixinProtocol",
) -> None:
    """
    Performs structural validation of a mixin class definition.
    Ensures that the mixin is safe to merge into dynamically generated
    instance classes.
    """

    # 1. __slots__ must be explicitly defined
    if "__slots__" not in cls.__dict__:
        raise_mixin_slots_is_not_defined(cls)

    # 2. Extract slot definition
    slots = cls.__dict__["__slots__"]

    # 3. __slots__ must be tuple or string
    if not isinstance(slots, (tuple, str)):
        raise_mixin_slots_unsuport_type(cls)

    # 4. All slot items must be strings
    slots_set = set(slots) if isinstance(slots, tuple) else {slots}
    if not all(isinstance(s, str) for s in slots_set):
        raise_mixin_slots_contain_unvalid_type(cls)

    # 5. __slots__ must not contain forbidden names
    if FORBIDDEN_NAMES & slots_set:
        raise_mixin_slots_contains_forbidden_slot_names(cls, slots_set)

    # 6. Class-level namespace must not contain forbidden names
    if FORBIDDEN_NAMES & cls.__dict__.keys():
        raise_mixin_dict_contains_forbidden_attributes(cls)

    # 7. Declarative flags must be boolean
    for flag in RESTRICTION_FLAGS:
        if flag in cls.__dict__ and not isinstance(cls.__dict__[flag], bool):
            raise_mixin_flag_is_not_bool(cls)

    # 8. _only_types must match supported structural forms
    if "_only_types" in cls.__dict__:
        only_types = cls.__dict__["_only_types"]
        if not (
            only_types is UNSET
            or isinstance(only_types, type)
            or (
                isinstance(only_types, tuple)
                and all(isinstance(item, type) for item in only_types)
            )
            or getattr(only_types, "__origin__", None) is Union
        ):
            raise_mixin_only_types_invalid(cls)

    # 9. init_mixins must call super().init_mixins()
    if "init_mixins" in cls.__dict__:
        func = cls.__dict__["init_mixins"]
        called_names = func.__code__.co_names
        if "super" not in called_names or "init_mixins" not in called_names:
            raise_mixin_init_mixins_missing_super_call(cls)


_DESIGN_NOTES = """
# verify_mixin_definition

## Purpose
Validates the structural correctness of a mixin class.  
Mixins are dynamically merged into runtime-generated instance classes, and
therefore must follow strict structural rules to ensure safety, determinism,
and compatibility.

This verifier ensures that a mixin:

- defines its own `__slots__`,
- uses valid slot types,
- does not collide with internal system attributes,
- declares valid restriction flags,
- defines `_only_types` correctly,
- preserves the initialization chain.

## Architectural reasoning
Mixins operate at the deepest level of the Simple system.  
They directly modify instance behavior, memory layout, and initialization flow.

Because mixins are merged dynamically, any structural mistake could:

- corrupt instance memory,
- override internal attributes,
- break reactive recalculation,
- shadow core properties,
- disrupt initialization order,
- cause unpredictable runtime failures.

This verifier prevents such issues by enforcing strict constraints.

## Validation pipeline
The validation steps are ordered intentionally:

1. **Presence of `__slots__`**  
   Mixins must define their own memory layout.

2. **Slot type validation**  
   Slots must be tuple or string.

3. **Slot item validation**  
   All items must be strings.

4. **Forbidden slot names**  
   Prevents overriding internal instance attributes.

5. **Forbidden class attributes**  
   Prevents overriding internal class-level API.

6. **Restriction flags**  
   Ensures compatibility constraints are boolean.

7. **`_only_types` validation**  
   Ensures type restrictions are structurally correct.

8. **Initialization chain validation**  
   Ensures mixins cooperate during instance initialization.

Each step isolates a specific structural concern.

## Diagnostic value
Every validation step delegates to a dedicated `raise_...` function that:

- computes the invalid values,
- formats a structured diagnostic message,
- provides actionable guidance,
- includes examples,
- preserves developer-friendly readability.

This makes debugging fast and predictable.

## Notes
- This verifier is executed automatically during class creation.
- It guarantees that only structurally valid mixins enter the system.
- It is a core safety mechanism of the Simple architecture.
"""