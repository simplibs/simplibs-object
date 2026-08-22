"""
Tests for `SimpleConstant.py`.

These public methods are thin wrappers around `_core/logic/constant_methods/*`.
These tests verify correct delegation to internal functions with the expected arguments.
"""
import pytest
from simplibs.object.exceptions import SimpleRuntimeError


class TestSimpleConstantDefaultValidate:

    def test_default_validate_accepts_any_type_matching_value(self, IntConst):
        assert IntConst._validate(999) is True


class TestSimpleConstantValidateTypeDelegation:

    def test_validate_type_delegates_correctly(self, IntConst):
        assert IntConst.validate_type(5) is True
        with pytest.raises(SimpleRuntimeError):
            IntConst.validate_type("wrong")


class TestSimpleConstantValidateDelegation:

    def test_validate_delegates_correctly(self, PositiveIntConst):
        assert PositiveIntConst.validate(1) is True
        with pytest.raises(SimpleRuntimeError):
            PositiveIntConst.validate(-1)


class TestSimpleConstantIsValid:

    def test_is_valid_is_shortcut_for_validate_return_bool_true(self, PositiveIntConst):
        assert PositiveIntConst.is_valid(1) is True
        assert PositiveIntConst.is_valid(-1) is False

    def test_is_valid_never_raises(self, PositiveIntConst):
        try:
            result = PositiveIntConst.is_valid("wrong-type")
        except SimpleRuntimeError:
            pytest.fail("is_valid must never raise an exception.")
        assert result is False


class TestSimpleConstantNormalizeDelegation:

    def test_normalize_delegates_correctly(self, IntConst):
        assert IntConst.normalize(5) == 5
        assert IntConst.normalize(None, process_none=True) == IntConst.meta.default


class TestSimpleConstantBoolOrRaiseValidateErrorDelegation:

    def test_bool_or_raise_delegates_correctly(self, IntConst):
        result = IntConst.bool_or_raise_validate_error(
            5, problem="test", return_bool=True
        )
        assert result is False