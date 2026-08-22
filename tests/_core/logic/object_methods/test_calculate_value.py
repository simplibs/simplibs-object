"""
Tests for `_core/logic/object_methods/calculate_value.py`.

Verifies integration between parameter resolution and class logic calculation.
"""
import pytest
from simplibs.object.exceptions import SimpleRuntimeError


class TestCalculateValueHappyPath:

    def test_calculates_via_positional_args(self, PairObject) -> None:
        """Verifies value calculation using positional arguments."""
        assert PairObject.calculate_value(2, 3) == 5

    def test_calculates_via_keyword_args(self, PairObject) -> None:
        """Verifies value calculation using keyword arguments."""
        assert PairObject.calculate_value(first=2, second=3) == 5

    def test_calculates_via_mixed_args(self, PairObject) -> None:
        """Verifies value calculation using combined positional and keyword arguments."""
        assert PairObject.calculate_value(2, second=3) == 5

    def test_missing_args_use_inner_defaults(self, PairObject) -> None:
        """Verifies calculation falls back to inner defaults when arguments are omitted."""
        assert PairObject.calculate_value() == 0


class TestCalculateValuePropagatesParamErrors:

    def test_unknown_kwarg_raises(self, PairObject) -> None:
        """Verifies unknown keyword arguments propagate error from parameter processing."""
        with pytest.raises(SimpleRuntimeError):
            PairObject.calculate_value(unknown=1)

    def test_too_many_positional_args_raises(self, PairObject) -> None:
        """Verifies excessive positional arguments propagate error from parameter processing."""
        with pytest.raises(SimpleRuntimeError):
            PairObject.calculate_value(1, 2, 3)