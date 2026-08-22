"""
Tests for `verify_down_limit(self, new_value, *, raise_exception=False)`.
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.methods.processors import (
    verify_down_limit,
)


class TestVerifyDownLimit:

    def test_no_limit_set_always_true(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        assert verify_down_limit(stepper, -(10**9)) is True

    def test_within_limit_returns_true(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 0
        assert verify_down_limit(stepper, 10) is True

    def test_below_limit_returns_false_without_raise(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 0
        assert verify_down_limit(stepper, -5) is False

    def test_below_limit_raises_when_requested(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 0
        with pytest.raises(Exception):
            verify_down_limit(stepper, -5, raise_exception=True)

    def test_action_triggered_on_limit_reached(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 0
        calls = []
        stepper.down_limit_action = lambda: calls.append(True)

        verify_down_limit(stepper, -1)

        assert calls == [True]