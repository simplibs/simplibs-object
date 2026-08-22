"""
Tests for `process_step_value(self, value=UNSET, *, validate=True)`.
"""
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.methods.processors import (
    process_step_value,
)


class TestProcessStepValue:

    def test_unset_returns_default_step(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_step_value(stepper)
        assert result == stepper.step

    def test_explicit_value_returned_normalized(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_step_value(stepper, 5)
        assert result == 5

    def test_custom_step_is_used_as_default(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.step = 3
        result = process_step_value(stepper)
        assert result == 3