import pytest
from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
# Outers
from ....testing.containers.TestMixin import TestMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


# noinspection PyTypeChecker
def assert_instance_creation(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that an instance of the target class can be created with mixins and verifies feature propagation.

    Instantiates the target blueprint class using ``TestMixin`` to ensure that mixin-driven
    dynamic instance creation correctly propagates slots, properties, methods, class attributes,
    and class methods down to the runtime object instance.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target class blueprint under test.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The instantiated runtime object created with ``TestMixin``.
    """
    subintro = "test_instance_creation::"

    # 1. Create instance with TestMixin
    instance = None
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=(TestMixin,))
        except Exception as exc:
            pytest.fail(f"Unexpected error during instance creation: {exc}")

        assert instance is not None, (
            f"Instantiating '{getattr(test_class, '__name__', test_class)}' with TestMixin returned None."
        )

    # 1.1 Guard clause: If the instance has not been created, we end the test
    if instance is None:
        return None

    # 2. Verify slot propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_slot_propagation",
        verbose=verbose,
    ):
        # noinspection PyProtectedMember
        assert instance._test_slot == "test_value", (
            f"Expected slot '_test_slot' to be 'test_value', got {instance._test_slot!r}."
        )

    # 3. Verify property propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_property_propagation",
        verbose=verbose,
    ):
        assert instance.test_property == "test_value", (
            f"Expected 'test_property' to be 'test_value', got {instance.test_property!r}."
        )

    # 4. Verify method propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_method_propagation",
        verbose=verbose,
    ):
        assert instance.test_method() == "[TestMixin] property=test_value", (
            f"Unexpected result of 'test_method()': {instance.test_method()!r}."
        )

    # 5. Verify class-level attribute propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_class_attribute",
        verbose=verbose,
    ):
        assert getattr(instance.__class__, "test_class_attribute", None) == "class_level_ok", (
            f"Expected class attribute 'test_class_attribute' to be 'class_level_ok', "
            f"got {getattr(instance.__class__, 'test_class_attribute', None)!r}."
        )

    # 6. Verify class-level method propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_class_method",
        verbose=verbose,
    ):
        assert instance.test_class_method() == "class_method_ok", (
            f"Unexpected result of 'test_class_method()': {instance.test_class_method()!r}."
        )

    return instance


_DESIGN_NOTES = """
# assert_instance_creation (Mixin-Enriched Instance Creation Gate)

## Purpose
Serves as a structural verification gate confirming that the metaclass and dynamic instance builder
can instantiate the target class blueprint while properly binding and propagating mixin capabilities.

## Verification Pipeline
The function executes a comprehensive check of mixin feature propagation across multiple architectural layers:
1. **Instantiation & Guard Gate:** Instantiates `test_class` with `mixins=(TestMixin,)`. If instantiation fails,
   a fail-fast guard terminates execution early to prevent downstream cascading errors on an uninitialized instance.
2. **Slot Propagation:** Confirms internal instance slots (`_test_slot`) are correctly allocated and initialized.
3. **Property Propagation:** Validates dynamic property getters (`test_property`).
4. **Instance Method Propagation:** Confirms instance methods (`test_method()`) execute and access instance state.
5. **Class-Level Attribute Propagation:** Verifies class attributes defined on mixins bind to the runtime class.
6. **Class-Level Method Propagation:** Verifies class methods (`test_class_method()`) operate smoothly on the instance interface.

## Pipeline Lifecycle Role
Acts as the second shallow gate inside composite orchestrators (e.g., `assert_simple_object`).
By returning the created `instance`, it allows downstream test stages to reuse a fully functional,
mixin-enriched object without requiring redundant instantiation calls.
"""
