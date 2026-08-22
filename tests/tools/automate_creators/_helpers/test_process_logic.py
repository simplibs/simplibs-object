"""
Tests for `tools/automate_creators/_helpers/process_logic.py`.
"""
from simplibs.object.tools.automate_creators._helpers.process_logic import process_logic


class TestProcessLogicRegularFunction:

    def test_regular_function_is_returned_unchanged(self):
        def my_logic(cls, first, second):
            return first + second

        result = process_logic(my_logic, ("first", "second"))
        assert result is my_logic


class TestProcessLogicLambda:

    def test_lambda_is_compiled_into_cls_prefixed_wrapper(self):
        sum_logic = lambda first, second: first + second

        wrapped = process_logic(sum_logic, ("first", "second"))
        assert wrapped is not sum_logic
        assert wrapped.__name__ == "_logic"

        assert wrapped(None, 2, 3) == 5

    def test_lambda_with_single_param(self):
        double_logic = lambda value: value * 2

        wrapped = process_logic(double_logic, ("value",))
        assert wrapped(None, 4) == 8

    def test_lambda_with_no_params(self):
        constant_logic = lambda: 42

        wrapped = process_logic(constant_logic, ())
        assert wrapped(None) == 42

    def test_params_name_order_is_preserved(self):
        subtract_logic = lambda first, second: first - second

        wrapped = process_logic(subtract_logic, ("first", "second"))
        assert wrapped(None, 10, 3) == 7