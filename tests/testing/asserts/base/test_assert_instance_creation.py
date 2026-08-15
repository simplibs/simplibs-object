import pytest
from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
# Outers
from ....testing.tools.TestMixin import TestMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


def assert_instance_creation(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """
    Creates an instance of the target class using TestMixin and verifies
    that all mixin-provided features propagate correctly.

    This is the second shallow gate used by assert_simple_object.
    """

    subintro = "test_instance_creation::"

    # 1. Create instance with TestMixin
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=(TestMixin,))
        except Exception as exc:
            pytest.fail(f"Unexpected error during instance creation: {exc}")

        assert instance is not None

    # 2. Verify slot propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_slot_propagation",
        verbose=verbose,
    ):
        # noinspection PyProtectedMember
        assert instance._test_slot == "test_value"

    # 3. Verify property propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_property_propagation",
        verbose=verbose,
    ):
        assert instance.test_property == "test_value"

    # 4. Verify method propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_method_propagation",
        verbose=verbose,
    ):
        assert instance.test_method() == "[TestMixin] property=test_value"

    # 5. Verify class-level attribute propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_class_attribute",
        verbose=verbose,
    ):
        assert getattr(instance.__class__, "test_class_attribute", None) == "class_level_ok"

    # 6. Verify class-level method propagation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_class_method",
        verbose=verbose,
    ):
        assert instance.test_class_method() == "class_method_ok"

    return instance
