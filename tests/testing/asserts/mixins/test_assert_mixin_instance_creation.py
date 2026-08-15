from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ....mixins.base_class import SimpleMixin
from ....SimpleConstant import SimpleConstant
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassType, SimpleMixinType


def assert_mixin_instance_creation(
    subtests: Any,
    mixin_class: "SimpleMixinType",
    test_class: "SimpleClassType",
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """
    Attempts to create an instance of `test_class` with the given mixin.

    Validates:
        - test_class is a valid SimpleObject/SimpleConstant class
        - mixin_class is compatible (SimpleMixin subclass)
        - instance creation succeeds
        - mixin is present in the MRO of the resulting instance

    Returns:
        The created instance with the mixin applied.
    """

    subintro = "assert_mixin_instance_creation::"

    # 1) Validate test_class inheritance
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_test_class",
        verbose=verbose,
    ):
        test_class: type
        if not issubclass(test_class, SimpleConstant):
            pytest.fail(
                f"Test class '{test_class.__name__}' must inherit from "
                f"SimpleConstant or SimpleObject."
            )

    # 2) Validate mixin identity (must be SimpleMixin subclass)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_mixin_class",
        verbose=verbose,
    ):
        mixin_class: type
        if not issubclass(mixin_class, SimpleMixin):
            pytest.fail(
                f"Mixin '{mixin_class.__name__}' does not inherit from SimpleMixin."
            )

    # 3) Attempt to create instance with mixin
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=(mixin_class,))
        except Exception as exc:
            pytest.fail(
                f"Failed to create instance of '{test_class.__name__}' "
                f"with mixin '{mixin_class.__name__}': {exc}"
            )

        if instance is None:
            pytest.fail(
                f"Instance creation returned None for class '{test_class.__name__}' "
                f"with mixin '{mixin_class.__name__}'."
            )

    # 4) Verify mixin is present in MRO
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}mixin_in_mro",
        verbose=verbose,
    ):
        if mixin_class not in instance.__class__.__mro__:
            pytest.fail(
                f"Mixin '{mixin_class.__name__}' is not present in the MRO of the "
                f"created instance. Instance class MRO: {instance.__class__.__mro__}"
            )

    return instance
