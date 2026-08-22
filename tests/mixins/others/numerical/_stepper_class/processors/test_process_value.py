"""
Tests for `process_value(self, value, *, validate=True)` (Stepper processor).
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.mixins.others.numerical._stepper_class.processors import process_value


class TestProcessValue:

    def test_returns_same_type_value_unchanged(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_value(stepper, 5)
        assert result == 5
        assert isinstance(result, int)

    def test_converts_to_instance_value_type(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_value(stepper, 5.0)
        assert isinstance(result, int)

    def test_validate_true_calls_instance_validate(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        with pytest.raises(Exception):
            process_value(stepper, "not_convertible_to_int_meaningfully")

    def test_validate_false_skips_validation(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        result = process_value(stepper, 3, validate=False)
        assert result == 3