import pytest
from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
from simplibs.sentinels import UNSET, UnsetType
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike
    from ...._core.protocols import SimpleMixinLike


def assert_user_instance_creation(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    mixins: tuple["SimpleMixinLike"] | UnsetType = UNSET,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """
    Creates a user-facing instance of the target class.

    - If mixins is UNSET → instance is created without mixins.
    - If mixins is a tuple → instance is created with these mixins.
    - Only verifies that instance creation succeeds.
    - Does NOT test mixin propagation (that is handled by assert_instance_creation).
    """

    subintro = "test_user_instance_creation::"

    # 1) Prepare mixins tuple
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_mixins",
        verbose=verbose,
    ):
        if mixins is UNSET:
            mixins_tuple = ()
        else:
            if not isinstance(mixins, tuple):
                pytest.fail("Parameter 'mixins' must be a tuple of mixin classes.")
            mixins_tuple = mixins

    # 2) Create instance with user mixins (or none)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=mixins_tuple)
        except Exception as exc:
            pytest.fail(
                f"Unexpected error during user instance creation "
                f"with mixins={mixins_tuple}: {exc}"
            )

        assert instance is not None

    return instance
