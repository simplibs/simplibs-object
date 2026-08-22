"""
Tests for `_core/logic/constant_methods/normalize.py`.

Verifies:
    1. None handling with `process_none` flag.
    2. Default value identity short-circuit optimization.
    3. Delegation to validation pipeline for non-default values.
"""
import pytest
from simplibs.object.exceptions import SimpleRuntimeError


class TestNormalizeNoneHandling:

    def test_none_with_process_none_true_returns_default(self, IntConst) -> None:
        """Verifies passing None with process_none=True resolves to default value."""
        assert IntConst.normalize(None, process_none=True) == IntConst.meta.default

    def test_none_with_process_none_false_raises(self, IntConst) -> None:
        """Verifies passing None with process_none=False raises SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            IntConst.normalize(None, process_none=False)

    def test_process_none_defaults_to_false(self, IntConst) -> None:
        """Verifies process_none defaults to False, rejecting None by default."""
        with pytest.raises(SimpleRuntimeError):
            IntConst.normalize(None)


class TestNormalizeDefaultIdentityOptimization:

    def test_value_equal_to_default_returns_default(self, IntConst) -> None:
        """Verifies default value comparison returns the default directly."""
        result = IntConst.normalize(IntConst.meta.default)
        assert result == IntConst.meta.default

    def test_value_equal_to_default_short_circuits_validation(self) -> None:
        """Verifies values equal to default bypass custom validation checks."""
        from simplibs.object import SimpleConstant

        class ZeroOnlyConst(SimpleConstant):
            _type = int
            _default = 0

            @classmethod
            def _validate(cls, value, *, return_bool=False):
                if value == cls._default:
                    return True
                return cls.bool_or_raise_validate_error(
                    value, problem="always rejects", return_bool=return_bool
                )

        assert ZeroOnlyConst.normalize(0) == 0


class TestNormalizeNonComparableValues:

    def test_non_comparable_value_falls_through_to_validation(self, IntConst) -> None:
        """Verifies objects raising on equality fall through to normal validation without crashing normalize."""

        class Unorderable:
            def __eq__(self, other):
                raise TypeError("cannot compare")

        with pytest.raises(SimpleRuntimeError):
            IntConst.normalize(Unorderable())


class TestNormalizeValidValue:

    def test_valid_value_is_returned_unchanged(self, IntConst) -> None:
        """Verifies valid values pass through normalize unchanged."""
        assert IntConst.normalize(42) == 42

    def test_invalid_value_raises_via_validate(self, IntConst) -> None:
        """Verifies invalid values trigger validation errors."""
        with pytest.raises(SimpleRuntimeError):
            IntConst.normalize("not-an-int")