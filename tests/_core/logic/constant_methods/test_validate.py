"""
Tests for `_core/logic/constant_methods/validate.py`.

Verifies validation pipeline orchestration across type checking and custom `_validate` logic.
"""
import pytest
from simplibs.object.exceptions import SimpleRuntimeError


class TestValidateHappyPath:

    def test_valid_value_passes_without_raising(self, IntConst) -> None:
        """Verifies valid value passes validation and returns True."""
        assert IntConst.validate(5) is True

    def test_positive_int_const_accepts_valid_value(self, PositiveIntConst) -> None:
        """Verifies custom validation passes conforming values."""
        assert PositiveIntConst.validate(10) is True


class TestValidateTypeFailure:

    def test_raises_on_wrong_type(self, IntConst) -> None:
        """Verifies type mismatch raises SimpleRuntimeError before reaching custom validation."""
        with pytest.raises(SimpleRuntimeError):
            IntConst.validate("wrong-type")

    def test_return_bool_true_returns_false_on_wrong_type(self, IntConst) -> None:
        """Verifies type mismatch returns False in boolean mode."""
        assert IntConst.validate("wrong-type", return_bool=True) is False


class TestValidateUserValidationFailure:

    def test_raises_when_custom_validate_rejects_value(self, PositiveIntConst) -> None:
        """Verifies custom validation logic failure raises SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            PositiveIntConst.validate(-5)

    def test_return_bool_true_returns_false_when_custom_validate_rejects(
        self, PositiveIntConst
    ) -> None:
        """Verifies custom validation failure returns False in boolean mode."""
        assert PositiveIntConst.validate(-5, return_bool=True) is False


class TestValidateUnexpectedException:

    def test_unexpected_exception_is_wrapped_into_simple_logic_error(self) -> None:
        """Verifies unexpected errors during validation are wrapped in SimpleRuntimeError."""
        from simplibs.object import SimpleConstant

        class ExplodingConst(SimpleConstant):
            _type = int
            _default = 0

            @classmethod
            def _validate(cls, value, *, return_bool=False):
                if value == 1:
                    raise RuntimeError("boom")
                return True

        with pytest.raises(SimpleRuntimeError):
            ExplodingConst.validate(1)

    def test_unexpected_exception_return_bool_true_returns_false(self) -> None:
        """Verifies unexpected errors during validation return False in boolean mode."""
        from simplibs.object import SimpleConstant

        class ExplodingConst(SimpleConstant):
            _type = int
            _default = 0

            @classmethod
            def _validate(cls, value, *, return_bool=False):
                if value == 1:
                    raise RuntimeError("boom")
                return True

        assert ExplodingConst.validate(1, return_bool=True) is False