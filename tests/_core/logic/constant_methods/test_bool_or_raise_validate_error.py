"""
Tests for `_core/logic/constant_methods/bool_or_raise_validate_error.py`.

Verifies validation error handling across exception raising and boolean return modes.
"""
import pytest
from simplibs.exception import SimpleException


class TestBoolOrRaiseValidateErrorRaiseMode:

    def test_raises_simple_exception_by_default(self, IntConst) -> None:
        """Verifies default behavior raises a SimpleException on validation failure."""
        with pytest.raises(SimpleException):
            IntConst.bool_or_raise_validate_error(5, problem="something is wrong")

    def test_raised_exception_wraps_value_error(self, IntConst) -> None:
        """Verifies the raised SimpleException contains standard exception payload."""
        with pytest.raises(SimpleException) as excinfo:
            IntConst.bool_or_raise_validate_error(5, problem="something is wrong")
        assert excinfo.value is not None


class TestBoolOrRaiseValidateErrorBoolMode:

    def test_return_bool_true_returns_false(self, IntConst) -> None:
        """Verifies return_bool=True suppresses exception and returns False on error."""
        result = IntConst.bool_or_raise_validate_error(
            5, problem="something is wrong", return_bool=True
        )
        assert result is False

    def test_return_bool_true_never_raises(self, IntConst) -> None:
        """Verifies return_bool=True guarantees no exceptions are propagated."""
        try:
            IntConst.bool_or_raise_validate_error(
                "anything", problem="whatever", return_bool=True
            )
        except SimpleException:
            pytest.fail("In bool mode, the function must not raise an exception.")