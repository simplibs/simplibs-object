"""
Tests for `process_up_limit_value(self, value)` (Stepper processor).
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.processors import (
    process_up_limit_value,
)


class TestProcessUpLimitValue:

    def test_set_up_limit_without_down_limit_first(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_up_limit_value(stepper, 100)
        assert result == 100

    def test_up_limit_above_down_limit_succeeds(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 0
        result = process_up_limit_value(stepper, 50)
        assert result == 50

    def test_up_limit_below_down_limit_raises(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = 10
        with pytest.raises(Exception):
            process_up_limit_value(stepper, 5)