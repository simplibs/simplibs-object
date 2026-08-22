"""
Tests for `tools/automate_creators/_helpers/_is_lambda.py`.
"""
from simplibs.object.tools.automate_creators._helpers._is_lambda import _is_lambda


class TestIsLambdaPositive:

    def test_lambda_is_detected(self):
        assert _is_lambda(lambda x: x) is True

    def test_lambda_with_no_args_is_detected(self):
        assert _is_lambda(lambda: None) is True


class TestIsLambdaNegative:

    def test_regular_function_is_not_lambda(self):
        def regular(x):
            return x

        assert _is_lambda(regular) is False

    def test_classmethod_function_is_not_lambda(self):
        class Foo:
            @classmethod
            def bar(cls, x):
                return x

        assert _is_lambda(Foo.bar) is False

    def test_builtin_function_is_not_lambda(self):
        assert _is_lambda(len) is False

    def test_non_callable_is_not_lambda(self):
        assert _is_lambda(42) is False
        assert _is_lambda("string") is False
        assert _is_lambda(None) is False

    def test_callable_object_without_dunder_name_is_not_lambda(self):
        class CallableObject:
            def __call__(self, x):
                return x

        assert _is_lambda(CallableObject()) is False

    def test_lambda_assigned_to_named_variable_is_still_detected(self):
        named_lambda = lambda x: x
        assert _is_lambda(named_lambda) is True