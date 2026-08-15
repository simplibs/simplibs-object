from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .asserts.base import assert_class_inheritance, assert_instance_creation, assert_user_instance_creation, assert_value_change
from .asserts.methods import assert_validate_method, assert_calculate_value_method, assert_decompose_value_method
from .asserts.reactivity import assert_reactivity_upward, assert_reactivity_downward
from .asserts.mutability import assert_mutable_behavior, assert_immutable_behavior
from .tools.InnerValue import InnerValue
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassLike, SimpleMixinLike


def assert_simple_object(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    mixins: tuple["SimpleMixinLike", ...] | UnsetType = UNSET,
    test_value_change: Any | InnerValue | UnsetType = UNSET,
    test_reactivity_up: InnerValue | UnsetType = UNSET,
    test_reactivity_down: Any | UnsetType = UNSET,
    test_mutability: Any | InnerValue | UnsetType = UNSET,
    test_immutability: Any | InnerValue | UnsetType = UNSET,
    verbose: bool = True,
    intro: str = "",
    deep_check: bool = True,
):
    """
    Unified shallow/deep validation pipeline for SimpleObject / SimpleConstant classes.

    Shallow:
        - verifies inheritance from SimpleConstant
        - instantiates object with a test mixin
        - verifies mixin propagation (slot + method)

    Deep:
        - validates default value
        - validates logic(defaults_of_inners)
        - validates decompose(default) if available
        - validates reactivity upward and downward
    """

    # ------------------------------------------------------------
    # SHALLOW TESTS - základní test
    # ------------------------------------------------------------

    # 1. Test předků
    assert_class_inheritance(
        subtests,
        test_class,
        verbose=verbose,
        intro=intro
    )

    # 2. Test vytvoření uživatelské instance (s mixiny a nebo bez pokud nejosou předané)
    instance = assert_user_instance_creation(
        subtests,
        test_class,
        mixins=mixins,
        verbose=verbose,
        intro=intro
    )

    # ------------------------------------------------------------
    # PARAMETER TESTS
    # ------------------------------------------------------------

    # 3. Test změny hodnoty
    if test_value_change is not UNSET:
        assert_value_change(
            subtests,
            instance,
            value=test_value_change,
            verbose=verbose,
            intro=intro
        )

    # 4. Test reaktivity směrem nahoru (pokud jsou předané data)
    verbose_value_change = test_value_change is UNSET
    if test_reactivity_up is not UNSET:
        # noinspection PyTypeChecker
        assert_reactivity_upward(
            subtests,
            instance,
            new_value=test_reactivity_up,
            verbose=verbose,
            verbose_value_change=verbose_value_change,
            intro=intro
        )

    # 5. Test reaktivity směrem dolu (pokud jsou předané data)
    if test_reactivity_down is not UNSET:
        verbose_value_change = verbose_value_change or test_reactivity_up is UNSET
        assert_reactivity_downward(
            subtests,
            instance,
            new_value=test_reactivity_down,
            verbose=verbose,
            verbose_value_change=verbose_value_change,
            intro=intro
        )

    # 5. Test měnosti
    if test_mutability is not UNSET:
        verbose_value_change = verbose_value_change or test_reactivity_down is UNSET
        assert_mutable_behavior(
            subtests,
            test_class,
            new_value=test_mutability,
            verbose=verbose,
            verbose_value_change=verbose_value_change,
            intro=intro
        )

    # 6. Test neměnosti
    if test_immutability is not UNSET:
        assert_immutable_behavior(
            subtests,
            test_class,
            new_value=test_immutability,
            verbose=verbose,
            intro=intro
        )

    # ------------------------------------------------------------
    # DEEP TESTS
    # ------------------------------------------------------------
    if deep_check:

        # 7. Test vytvoření instance (pomocí testovacího mixinu)
        assert_instance_creation(
            subtests,
            test_class,
            verbose=verbose,
            intro=intro
        )

        # 8. Running test metody validate
        if "_validate" in test_class.__dict__:
            assert_validate_method(
                subtests,
                test_class,
                verbose=verbose,
                intro=intro
            )

        # 9. Running test metody calculate_value (pouze pro kompozice)
        if "_logic" in test_class.__dict__:
            assert_calculate_value_method(
                subtests,
                test_class,
                verbose=verbose,
                intro=intro
            )

        # 10. Running test metody decompose_value (pouze pokud je třída rozložitelná)
        if "_decompose" in test_class.__dict__ and test_class.meta.is_decomposeable:
            assert_decompose_value_method(
                subtests,
                test_class,
                verbose=verbose,
                intro=intro
            )

    return instance
