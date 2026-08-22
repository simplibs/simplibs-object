"""
Tests for `tools/automate_creators/_helpers/process_validate.py`.
"""
from simplibs.object.tools.automate_creators._helpers.process_validate import (
    process_validate,
)


class TestProcessValidateRegularFunction:

    def test_regular_function_is_returned_unchanged(self):
        def my_validate(cls, value, *, return_bool=False):
            return value > 0

        result = process_validate(my_validate)
        assert result is my_validate


class TestProcessValidateLambda:

    def test_lambda_is_wrapped_into_classmethod_compatible_signature(self):
        validate_positive = lambda value: value > 0

        wrapped = process_validate(validate_positive)
        assert wrapped is not validate_positive

        assert wrapped(None, 5) is True
        assert wrapped(None, -5) is False

    def test_wrapped_lambda_accepts_return_bool_kwarg(self):
        validate_positive = lambda value: value > 0
        wrapped = process_validate(validate_positive)

        assert wrapped(None, 5, return_bool=True) is True

    def test_wrapped_lambda_only_uses_value_argument(self):
        calls = []
        validate_fn = lambda value: calls.append(value) or True
        wrapped = process_validate(validate_fn)

        wrapped(None, "only-value-should-be-passed")
        assert calls == ["only-value-should-be-passed"]