"""
Tests for `step_up(self, value=UNSET, *, validate=True, raise_exception=False)`.
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.methods import step_up


class TestStepUp:

    def test_default_step_increments_by_one(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        original = instance._value
        result = step_up(stepper)
        assert result is True
        assert instance._value == original + 1

    def test_custom_value_increments_by_given_amount(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        original = instance._value
        step_up(stepper, 5)
        assert instance._value == original + 5

    def test_exceeding_up_limit_returns_false(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = instance._value
        result = step_up(stepper)
        assert result is False

    def test_exceeding_up_limit_does_not_modify_value(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = instance._value
        original = instance._value
        step_up(stepper)
        assert instance._value == original

    def test_exceeding_up_limit_raises_when_requested(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = instance._value
        with pytest.raises(Exception):
            step_up(stepper, raise_exception=True)