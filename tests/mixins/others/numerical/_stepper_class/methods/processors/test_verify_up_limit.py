"""
Tests for `verify_up_limit(self, new_value, *, raise_exception=False)`.
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.methods.processors import (
    verify_up_limit,
)


class TestVerifyUpLimit:

    def test_no_limit_set_always_true(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        assert verify_up_limit(stepper, 10**9) is True

    def test_within_limit_returns_true(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 100
        assert verify_up_limit(stepper, 50) is True

    def test_exceeding_limit_returns_false_without_raise(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        assert verify_up_limit(stepper, 20) is False

    def test_exceeding_limit_raises_when_requested(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        with pytest.raises(Exception):
            verify_up_limit(stepper, 20, raise_exception=True)

    def test_action_triggered_on_limit_exceeded(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        calls = []
        stepper.up_limit_action = lambda: calls.append(True)

        verify_up_limit(stepper, 20)

        assert calls == [True]

    def test_action_not_triggered_within_limit(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        calls = []
        stepper.up_limit_action = lambda: calls.append(True)

        verify_up_limit(stepper, 5)

        assert calls == []