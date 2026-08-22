"""
Tests for `set_value(self, value, *, validate=True, raise_exception=False)`.
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.methods import set_value


class TestSetValue:

    def test_sets_new_value_and_returns_true(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = set_value(stepper, 42)
        assert result is True
        assert instance._value == 42

    def test_identical_value_is_noop_returns_true(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        current = instance._value
        result = set_value(stepper, current)
        assert result is True
        assert instance._value == current

    def test_exceeding_up_limit_returns_false(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        result = set_value(stepper, 100)
        assert result is False
        assert instance._value != 100

    def test_below_down_limit_returns_false(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 0
        result = set_value(stepper, -100)
        assert result is False
        assert instance._value != -100

    def test_exceeding_limit_raises_when_requested(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        with pytest.raises(Exception):
            set_value(stepper, 100, raise_exception=True)