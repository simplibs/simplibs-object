"""
Tests for `process_down_limit_value(self, value)` (Stepper processor).
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.processors import (
    process_down_limit_value,
)


class TestProcessDownLimitValue:

    def test_set_down_limit_without_up_limit_first(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_down_limit_value(stepper, -10)
        assert result == -10

    def test_down_limit_below_up_limit_succeeds(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 100
        result = process_down_limit_value(stepper, 0)
        assert result == 0

    def test_down_limit_above_up_limit_raises(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 10
        with pytest.raises(Exception):
            process_down_limit_value(stepper, 20)