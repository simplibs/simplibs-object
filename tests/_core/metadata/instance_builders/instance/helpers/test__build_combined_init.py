"""
Tests for `_core/metadata/instance_builders/instance/helpers/_build_combined_init_mixins.py`.
"""
import pytest
from simplibs.object._core.metadata.instance_builders.instance.helpers._build_combined_init_mixins import (
    _build_combined_init_mixins,
)


class TestBuildCombinedInitMixinsSequentialExecution:

    def test_calls_all_hooks_in_order(self):
        calls = []

        def hook_a(self):
            calls.append("a")

        def hook_b(self):
            calls.append("b")

        combined = _build_combined_init_mixins([hook_a, hook_b])
        combined(object())

        assert calls == ["a", "b"]

    def test_each_hook_receives_the_same_self(self):
        received = []

        def hook_a(self):
            received.append(self)

        def hook_b(self):
            received.append(self)

        combined = _build_combined_init_mixins([hook_a, hook_b])
        target = object()
        combined(target)

        assert received == [target, target]


class TestBuildCombinedInitMixinsEmptyHooks:

    def test_empty_hooks_list_is_a_noop(self):
        combined = _build_combined_init_mixins([])
        # Must execute without raising an exception
        combined(object())


class TestBuildCombinedInitMixinsSingleHook:

    def test_single_hook_is_invoked_once(self):
        calls = []

        def hook(self):
            calls.append(1)

        combined = _build_combined_init_mixins([hook])
        combined(object())

        assert calls == [1]


class TestBuildCombinedInitMixinsExceptionHandling:

    def test_exception_in_hook_propagates_and_stops_execution(self):
        calls = []

        def hook_a(self):
            calls.append("a")

        def hook_failing(self):
            raise ValueError("Hook initialization failed")

        def hook_b(self):
            calls.append("b")

        combined = _build_combined_init_mixins([hook_a, hook_failing, hook_b])

        with pytest.raises(ValueError, match="Hook initialization failed"):
            combined(object())

        assert calls == ["a"]