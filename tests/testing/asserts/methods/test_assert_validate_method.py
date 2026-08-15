from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
from simplibs.exception.testing import maybe_subtest
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


def assert_validate_method(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Deep validation gate:
        - validates that the class default passes full validation
        - validates that invalid values (UNSET, None) fail validation
    """

    subintro = "test_validate_default::"

    # 1. Default must pass validation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_default_pass",
        verbose=verbose,
    ):
        default = test_class.meta.default
        assert test_class.validate(default, return_bool=True)

    # 2. UNSET must fail (return_bool=True)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_unset_fail_bool",
        verbose=verbose,
    ):
        assert test_class.validate(UNSET, return_bool=True) is False

    # 3. UNSET must fail (return_bool=False → exception)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_unset_fail_exception",
        verbose=verbose,
    ):
        # noinspection PyBroadException
        try:
            test_class.validate(UNSET, return_bool=False)
        except Exception:
            pass
        else:
            raise AssertionError("validate(UNSET) did not raise an exception")

    # 4. None must fail (return_bool=True)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_none_fail_bool",
        verbose=verbose,
    ):
        assert test_class.validate(None, return_bool=True) is False

    # 5. None must fail (return_bool=False → exception)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_none_fail_exception",
        verbose=verbose,
    ):
        # noinspection PyBroadException
        try:
            test_class.validate(None, return_bool=False)
        except Exception:
            pass
        else:
            raise AssertionError("validate(None) did not raise an exception")
