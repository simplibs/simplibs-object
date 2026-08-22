from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .asserts.base import (
    assert_class_inheritance,
    assert_instance_creation,
    assert_user_instance_creation,
    assert_value_change,
)
from .asserts.methods import (
    assert_validate_method,
    assert_calculate_value_method,
    assert_decompose_value_method,
)
from .asserts.reactivity import (
    assert_reactivity_upward,
    assert_reactivity_downward
)
from .asserts.mutability import (
    assert_mutable_behavior,
    assert_immutable_behavior
)
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassLike, SimpleMixinLike
    from .containers.InnerValue import InnerValue


def assert_simple_object(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    mixins: tuple["SimpleMixinLike", ...] | UnsetType = UNSET,
    test_value_change: "Any | InnerValue | UnsetType" = UNSET,
    test_reactivity_up: "InnerValue | UnsetType" = UNSET,
    test_reactivity_down: "Any | UnsetType" = UNSET,
    test_mutability: "Any | InnerValue | UnsetType" = UNSET,
    test_immutability: "Any | InnerValue | UnsetType" = UNSET,
    verbose: bool = True,
    intro: str = "",
    deep_check: bool = True,
) -> Any:
    """Unified master test runner executing shallow, deep, and parameter assertions on object classes.

    Executes an orchestrated pipeline validating class hierarchy, default instantiation, mixin binding,
    state mutations, upward/downward reactivity cascades, mutability contracts, and internal lifecycle
    methods (``_validate``, ``_logic``, ``_decompose``).

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target object blueprint class under test.
        mixins: Optional tuple of mixin classes to inject during user instance instantiation.
        test_value_change: Candidate value or ``InnerValue`` payload used to test state changes.
        test_reactivity_up: ``InnerValue`` payload used to verify upward state recalculation.
        test_reactivity_down: Raw composite value used to verify downward decomposition cascades.
        test_mutability: Raw value used to test in-place state mutation preserving object identity.
        test_immutability: Raw value used to test state changes returning new object instances.
        verbose: Enables isolated pytest subtests reporting across child assertions.
        intro: Optional prefix string added to generated subtest identity names.
        deep_check: Enables deep structural checks (synthetic mixin injection, internal methods verification).

    Returns:
        The created user instance with optional mixins applied.
    """

    # ------------------------------------------------------------
    # 1. SHALLOW TESTS (Base instantiation & inheritance)
    # ------------------------------------------------------------

    # Verify inheritance from SimpleConstant / SimpleObject base
    assert_class_inheritance(
        subtests,
        test_class,
        verbose=verbose,
        intro=intro,
    )

    # Instantiate user target instance (with provided mixins or defaults)
    instance = assert_user_instance_creation(
        subtests,
        test_class,
        mixins=mixins,
        verbose=verbose,
        intro=intro,
    )

    # ------------------------------------------------------------
    # 2. PARAMETER TESTS (State mutation, reactivity & mutability)
    # ------------------------------------------------------------

    # Test direct value change on the live instance
    if test_value_change is not UNSET:
        assert_value_change(
            subtests,
            instance,
            value=test_value_change,
            verbose=verbose,
            intro=intro,
        )

    # Test upward reactivity (leaf to root recalculation)
    verbose_value_change = test_value_change is UNSET
    if test_reactivity_up is not UNSET:
        # noinspection PyTypeChecker
        assert_reactivity_upward(
            subtests,
            instance,
            new_value=test_reactivity_up,
            verbose=verbose,
            verbose_value_change=verbose_value_change,
            intro=intro,
        )

    # Test downward reactivity (root to leaves decomposition cascade)
    if test_reactivity_down is not UNSET:
        verbose_value_change = verbose_value_change or test_reactivity_up is UNSET
        assert_reactivity_downward(
            subtests,
            instance,
            new_value=test_reactivity_down,
            verbose=verbose,
            verbose_value_change=verbose_value_change,
            intro=intro,
        )

    # Test mutable behavior contract (in-place modification preserving identity)
    if test_mutability is not UNSET:
        verbose_value_change = verbose_value_change or test_reactivity_down is UNSET
        assert_mutable_behavior(
            subtests,
            test_class,
            new_value=test_mutability,
            verbose=verbose,
            verbose_value_change=verbose_value_change,
            intro=intro,
        )

    # Test immutable behavior contract (state update returning a new instance identity)
    if test_immutability is not UNSET:
        assert_immutable_behavior(
            subtests,
            test_class,
            new_value=test_immutability,
            verbose=verbose,
            intro=intro,
        )

    # ------------------------------------------------------------
    # 3. DEEP TESTS (Synthetic mixin injection & internal methods)
    # ------------------------------------------------------------
    if deep_check:

        # Synthetic instance creation with internal test mixin attached
        assert_instance_creation(
            subtests,
            test_class,
            verbose=verbose,
            intro=intro,
        )

        # Run direct unit test on internal _validate method if overridden
        if "_validate" in test_class.__dict__:
            assert_validate_method(
                subtests,
                test_class,
                verbose=verbose,
                intro=intro,
            )

        # Run direct unit test on internal _logic method if overridden (composites)
        if "_logic" in test_class.__dict__:
            assert_calculate_value_method(
                subtests,
                test_class,
                verbose=verbose,
                intro=intro,
            )

        # Run direct unit test on internal _decompose method if overridden and class is decomposeable
        if "_decompose" in test_class.__dict__ and test_class.meta.is_decomposeable:
            assert_decompose_value_method(
                subtests,
                test_class,
                verbose=verbose,
                intro=intro,
            )

    return instance


_DESIGN_NOTES = """
# assert_simple_object (Master Object Testing Orchestrator)

## Purpose
Serves as the primary end-to-end testing pipeline entry point for verifying the compliance and structural 
integrity of `SimpleObject` and `SimpleConstant` class implementations. It unifies shallow structural checks, 
state mutation parameters, behavioral reactivity pipelines, and deep framework lifecycle validation into 
a single high-level runner.

## Execution Stages & Cascading Verbosity
1. **Shallow Suite:**
   - `assert_class_inheritance`: Asserts inheritance hierarchy requirements.
   - `assert_user_instance_creation`: Instantiates a user object (optionally bound with mixins).
2. **Parameter Suite (Opt-in via non-UNSET arguments):**
   - Direct value mutation via `assert_value_change`.
   - Upward reactivity cascades via `assert_reactivity_upward`.
   - Downward decomposition cascades via `assert_reactivity_downward`.
   - In-place mutable state behavior via `assert_mutable_behavior`.
   - Identity-changing immutable state behavior via `assert_immutable_behavior`.
   - *Verbosity Cascade Control:* Dynamically manages `verbose_value_change` flags across child assertions 
     to avoid redundant subtest report spamming when nested mutations occur.
3. **Deep Suite (`deep_check=True`):**
   - Injects a synthetic testing mixin via `assert_instance_creation` to guarantee subclass dynamic mixin stability.
   - Direct isolated method testing for `_validate`, `_logic` (composite calculation), and `_decompose`.

## Returns
Returns the live user instance created in Step 1, allowing calling unit tests to perform additional custom 
assertions post-orchestration.
"""