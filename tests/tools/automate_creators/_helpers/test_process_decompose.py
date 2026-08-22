"""
Tests for `tools/automate_creators/_helpers/process_decompose.py`.
"""
from simplibs.object.tools.automate_creators._helpers.process_decompose import (
    process_decompose,
)


class TestProcessDecomposeRegularFunction:

    def test_regular_function_is_returned_unchanged(self):
        def my_decompose(cls, value):
            return (value, 0)

        result = process_decompose(my_decompose)
        assert result is my_decompose


class TestProcessDecomposeLambda:

    def test_lambda_is_wrapped_into_cls_prefixed_signature(self):
        split_decompose = lambda value: (value, 0)

        wrapped = process_decompose(split_decompose)
        assert wrapped is not split_decompose

        assert wrapped(None, 5) == (5, 0)

    def test_wrapped_lambda_ignores_cls_argument(self):
        calls = []
        decompose_fn = lambda value: calls.append(value) or (value,)
        wrapped = process_decompose(decompose_fn)

        wrapped("ignored-cls", 7)
        assert calls == [7]