"""
Tests for `_core/logic/constant_methods/validate_type.py`.

Verifies type-level checking and error raising against configured metadata types.
"""
import pytest
from simplibs.object.exceptions import SimpleRuntimeError


class TestValidateTypeHappyPath:

    def test_returns_true_when_value_matches_type(self, IntConst) -> None:
        """Verifies matching type returns True."""
        assert IntConst.validate_type(5) is True

    def test_returns_true_for_default_value(self, IntConst) -> None:
        """Verifies default value matches declared type."""
        assert IntConst.validate_type(IntConst.meta.default) is True


class TestValidateTypeMismatch:

    def test_raises_simple_logic_error_by_default(self, IntConst) -> None:
        """Verifies type mismatch raises SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            IntConst.validate_type("not-an-int")

    def test_return_bool_true_returns_false_instead_of_raising(self, IntConst) -> None:
        """Verifies type mismatch returns False when return_bool=True."""
        assert IntConst.validate_type("not-an-int", return_bool=True) is False

    def test_return_bool_true_does_not_raise(self, IntConst) -> None:
        """Verifies boolean mode never raises an exception on type mismatch."""
        try:
            result = IntConst.validate_type(3.14, return_bool=True)
        except SimpleRuntimeError:
            pytest.fail("validate_type(return_bool=True) should not raise an exception.")
        assert result is False


class TestValidateTypeEdgeCases:

    def test_bool_is_not_valid_int_edge_case_not_asserted(self, IntConst) -> None:
        """Documents Python standard type hierarchy where bool is a subclass of int."""
        assert IntConst.validate_type(True) is True