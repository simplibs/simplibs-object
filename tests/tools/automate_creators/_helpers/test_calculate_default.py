"""
Tests for `tools/automate_creators/_helpers/calculate_default.py`.
"""
import pytest
from simplibs.object.tools.automate_creators._helpers.calculate_default import (
    calculate_default,
)


class TestCalculateDefaultHappyPath:

    def test_calculates_result_using_default_params(self):
        def logic(cls, first, second):
            return first + second

        result = calculate_default(logic, (2, 3))
        assert result == 5

    def test_calls_with_cls_as_none(self):
        received = {}

        def logic(cls, value):
            received["cls"] = cls
            return value

        calculate_default(logic, (1,))
        assert received["cls"] is None

    def test_empty_params_tuple(self):
        def logic(cls):
            return 42

        assert calculate_default(logic, ()) == 42


class TestCalculateDefaultFailure:

    def test_exception_during_execution_is_wrapped(self):
        def exploding_logic(cls, value):
            raise RuntimeError("boom")

        with pytest.raises(Exception):
            calculate_default(exploding_logic, (1,))

    def test_wrong_arity_callable_raises(self):
        raw_lambda = lambda first, second: first + second

        with pytest.raises(Exception):
            calculate_default(raw_lambda, (2, 3))