from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .asserts.mixins import (
    assert_mixin_inheritance,
    assert_mixin_instance_creation,
    assert_instance_hasattr,
    assert_mixins_slots_values,
)
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassType, SimpleMixinType


def assert_simple_mixin(
    subtests: Any,
    mixin_class: "SimpleMixinType",
    *,
    test_class: "SimpleClassType",
    mutable: bool = True,
    slots_names: tuple[str, ...] | UnsetType = UNSET,
    slots_values: tuple[tuple[str, Any], ...] | tuple[str, Any] | UnsetType = UNSET,
    attribute_names: tuple[str, ...] | UnsetType = UNSET,
    method_names: tuple[str, ...] | UnsetType = UNSET,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Unified master test runner executing compliance and structure assertions on mixin classes.

    Executes an orchestrated pipeline validating base mixin inheritance, dynamic binding and MRO
    injection onto a target blueprint class, slot presence and state initialization, attribute presence,
    and method existence.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        mixin_class: Target mixin class blueprint under test.
        test_class: Base blueprint class used to instantiate and bind the mixin.
        mutable: Defines whether the underlying instance should be created in mutable mode (default True).
        slots_names: Optional tuple of expected slot string identifiers to check for presence.
        slots_values: Optional tuple of single or multiple ``(slot_name, expected_value)`` pairs.
        attribute_names: Optional tuple of expected attribute identifiers to check for presence.
        method_names: Optional tuple of expected method identifiers to check for presence.
        verbose: Enables isolated pytest subtests reporting across child assertions.
        intro: Optional prefix string added to generated subtest identity names.

    Returns:
        The created instance with the mixin applied for potential downstream user tests.
    """

    # ------------------------------------------------------------
    # 1. SHALLOW TESTS (Base Mixin Inheritance & Instantiation)
    # ------------------------------------------------------------

    # Verify mixin class inherits from SimpleMixin
    assert_mixin_inheritance(
        subtests,
        mixin_class,
        verbose=verbose,
        intro=intro,
    )

    # Instantiate test_class with mixin attached and verify MRO injection
    instance = assert_mixin_instance_creation(
        subtests,
        mixin_class,
        test_class,
        mutable=mutable,
        verbose=verbose,
        intro=intro,
    )

    if instance is None:
        return None

    # ------------------------------------------------------------
    # 2. PARAMETER TESTS (Structural & Member Verification)
    # ------------------------------------------------------------

    # Assert presence of expected slot names
    if slots_names is not UNSET:
        slots_names: tuple[str, ...]
        assert_instance_hasattr(
            subtests,
            instance,
            names=slots_names,
            kind="slot",
            verbose=verbose,
            intro=intro,
        )

    # Assert expected slot values on the initialized instance
    if slots_values is not UNSET:
        assert_mixins_slots_values(
            subtests,
            instance,
            slots_values=slots_values,
            verbose=verbose,
            intro=intro,
        )

    # Assert presence of expected general attribute names
    if attribute_names is not UNSET:
        attribute_names: tuple[str, ...]
        assert_instance_hasattr(
            subtests,
            instance,
            names=attribute_names,
            kind="attribute",
            verbose=verbose,
            intro=intro,
        )

    # Assert presence of expected method names
    if method_names is not UNSET:
        method_names: tuple[str, ...]
        assert_instance_hasattr(
            subtests,
            instance,
            names=method_names,
            kind="method",
            verbose=verbose,
            intro=intro,
        )

    return instance


_DESIGN_NOTES = """
# assert_simple_mixin (Master Mixin Testing Orchestrator)

## Purpose
Acts as the primary orchestrator for validating `SimpleMixin` subclasses and their integration with 
the framework's dynamic instance construction mechanism. It ensures base inheritance compliance, 
proper Method Resolution Order (MRO) injection, and structural propagation of slots, attributes, and methods.

## Verification Stages
1. **Shallow Suite (Core Contract):**
   - `assert_mixin_inheritance`: Verifies that `mixin_class` derives directly or indirectly from `SimpleMixin`.
   - `assert_mixin_instance_creation`: Binds `mixin_class` onto `test_class` via `test_class(mixins=(mixin_class,))`, 
     verifying creation success and presence in `instance.__class__.__mro__`.
2. **Parameter Suite (Opt-in Member Verification):**
   - Slots Presence Gate (`slots_names`): Delegates to `assert_instance_hasattr[slot]`.
   - Slots Value Reconciliation (`slots_values`): Delegates to `assert_mixins_slots_values`.
   - Attributes Presence Gate (`attribute_names`): Delegates to `assert_instance_hasattr[attribute]`.
   - Methods Presence Gate (`method_names`): Delegates to `assert_instance_hasattr[method]`.

## Returns
Returns the instantiated `instance` carrying the injected mixin, allowing callers to execute 
custom runtime assertions or method calls on the live object.
"""