"""
Tests for `_core/logic/object_methods/_process_calculate_value_params.py`.

Verifies argument binding, default filling, type validation, and collision detection.
"""
import pytest
from simplibs.object._core.logic.object_methods._process_calculate_value_params import (
    _process_calculate_value_params,
)
from simplibs.object.exceptions import SimpleRuntimeError


class TestProcessParamsPositional:

    def test_all_positional(self, PairObject) -> None:
        """Verifies full positional mapping to inner parameters."""
        result = _process_calculate_value_params(PairObject, 1, 2)
        assert result == {"first": 1, "second": 2}

    def test_partial_positional_rest_defaults(self, PairObject) -> None:
        """Verifies partial positional arguments populate remaining keys with inner defaults."""
        result = _process_calculate_value_params(PairObject, 5)
        assert result == {"first": 5, "second": 0}

    def test_no_args_all_defaults(self, PairObject) -> None:
        """Verifies omitting arguments fills all keys with their inner defaults."""
        result = _process_calculate_value_params(PairObject)
        assert result == {"first": 0, "second": 0}


class TestProcessParamsKeyword:

    def test_all_keyword(self, PairObject) -> None:
        """Verifies complete keyword argument mapping."""
        result = _process_calculate_value_params(PairObject, first=1, second=2)
        assert result == {"first": 1, "second": 2}

    def test_mixed_positional_and_keyword(self, PairObject) -> None:
        """Verifies mixed positional and keyword argument resolution."""
        result = _process_calculate_value_params(PairObject, 1, second=2)
        assert result == {"first": 1, "second": 2}


class TestProcessParamsErrors:

    def test_too_many_positional_args_raises(self, PairObject) -> None:
        """Verifies exceeding positional argument count raises SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            _process_calculate_value_params(PairObject, 1, 2, 3)

    def test_duplicate_argument_raises(self, PairObject) -> None:
        """Verifies passing parameter both positionally and by keyword raises SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            _process_calculate_value_params(PairObject, 1, first=1)

    def test_unknown_keyword_argument_raises(self, PairObject) -> None:
        """Verifies unknown keyword arguments raise SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            _process_calculate_value_params(PairObject, unknown=1)

    def test_value_is_validated_against_inner_type(self, PairObject) -> None:
        """Verifies arguments failing inner type validation raise SimpleRuntimeError."""
        with pytest.raises(SimpleRuntimeError):
            _process_calculate_value_params(PairObject, "not-an-int")