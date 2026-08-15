from typing import Any, TYPE_CHECKING
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing import maybe_subtest
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


# noinspection PyTypeChecker
def assert_validate_method(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that the target class method ``validate`` behaves correctly across valid and invalid inputs.

    Executes a multi-stage validation check on the class blueprint:
    verifies that the class default value passes validation, while invalid sentinels and values
    (e.g., ``UNSET``, ``None``) consistently fail validation across both boolean mode
    (``return_bool=True``) and exception mode (``return_bool=False``).

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target class blueprint under test.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_validate_default::"

    # 1. Class default value must pass validation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_default_pass",
        verbose=verbose,
    ):
        default = test_class.meta.default
        assert test_class.validate(default, return_bool=True), (
            f"Default value '{default!r}' failed validation for '{test_class.__name__}'."
        )

    # 2. UNSET sentinel must fail validation in boolean mode
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_unset_fail_bool",
        verbose=verbose,
    ):
        assert test_class.validate(UNSET, return_bool=True) is False, (
            f"validate(UNSET, return_bool=True) expected False for '{test_class.__name__}'."
        )

    # 3. UNSET sentinel must raise an exception in non-boolean mode
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_unset_fail_exception",
        verbose=verbose,
    ):
        try:
            test_class.validate(UNSET, return_bool=False)
        except Exception:
            pass
        else:
            pytest.fail(f"validate(UNSET, return_bool=False) did not raise an exception for '{test_class.__name__}'.")

    # 4. None value must fail validation in boolean mode
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_none_fail_bool",
        verbose=verbose,
    ):
        assert test_class.validate(None, return_bool=True) is False, (
            f"validate(None, return_bool=True) expected False for '{test_class.__name__}'."
        )

    # 5. None value must raise an exception in non-boolean mode
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_none_fail_exception",
        verbose=verbose,
    ):
        try:
            test_class.validate(None, return_bool=False)
        except Exception:
            pass
        else:
            pytest.fail(f"validate(None, return_bool=False) did not raise an exception for '{test_class.__name__}'.")


_DESIGN_NOTES = """
# assert_validate_method (Validation Engine Structural Gate)

## Purpose
Verifies that the target blueprint class implements a robust validation engine (`validate`). 
It guarantees that valid default values pass validation seamlessly while invalid inputs 
(specifically `UNSET` and `None`) fail deterministically in both boolean and exception modes.

## Validation Matrix
1. **Valid Default Pass:** Asserts `test_class.validate(default, return_bool=True) == True` for 
   the class's own declared metadata default.
2. **`UNSET` Boolean Rejection:** Asserts `validate(UNSET, return_bool=True) == False`.
3. **`UNSET` Exception Rejection:** Asserts `validate(UNSET, return_bool=False)` raises a validation exception.
4. **`None` Boolean Rejection:** Asserts `validate(None, return_bool=True) == False`.
5. **`None` Exception Rejection:** Asserts `validate(None, return_bool=False)` raises a validation exception.

## Pipeline Lifecycle Role
Serves as an essential method-level quality gate within orchestrators like `assert_simple_object`. 
By verifying validation mechanics prior to runtime instance mutation tests, it prevents false-positive 
passes and confirms that error handling behaves consistently across dual validation modes.
"""