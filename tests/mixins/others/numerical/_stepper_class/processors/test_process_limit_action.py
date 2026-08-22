"""
Tests for `process_limit_action(self, value)` (Stepper processor).
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.processors import (
    process_limit_action,
)


class TestProcessLimitAction:

    def test_callable_returned_unchanged(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)

        def my_action():
            pass

        result = process_limit_action(stepper, my_action)
        assert result is my_action

    def test_non_callable_raises(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        with pytest.raises(Exception):
            process_limit_action(stepper, "not_callable")

    def test_lambda_is_accepted(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_limit_action(stepper, lambda: None)
        assert callable(result)