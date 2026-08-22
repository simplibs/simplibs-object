"""
Tests for `Stepper` service class.
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class import Stepper


class TestStepperConstruction:

    def test_binds_instance(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        assert stepper._instance is instance

    def test_default_step_is_one(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        assert stepper.step == 1

    def test_default_limits_are_unset(self, IntLeaf):
        from simplibs.sentinels import UNSET
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        assert stepper.up_limit is UNSET
        assert stepper.down_limit is UNSET
        assert stepper.up_limit_action is UNSET
        assert stepper.down_limit_action is UNSET

    def test_value_type_inferred_from_instance(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        assert stepper._value_type is int

    def test_rejects_non_numeric_instance(self):
        from simplibs.object import SimpleConstant

        class StrLeaf(SimpleConstant):
            _type = str
            _default = "x"

        instance = StrLeaf(as_atom=True, mutable=True)
        with pytest.raises(Exception):
            Stepper(instance)


class TestStepperProperties:

    def test_step_setter_normalizes_value(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.step = 5
        assert stepper.step == 5

    def test_up_limit_setter(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.up_limit = 100
        assert stepper.up_limit == 100

    def test_down_limit_setter(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.down_limit = -100
        assert stepper.down_limit == -100


class TestStepperMethods:

    def test_step_up_method(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        original = instance._value
        stepper.step_up()
        assert instance._value == original + 1

    def test_step_down_method(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        original = instance._value
        stepper.step_down()
        assert instance._value == original - 1

    def test_set_value_method(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        stepper.set_value(999)
        assert instance._value == 999


class TestStepperRepr:

    def test_repr_contains_value_and_step(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        stepper = Stepper(instance)
        text = repr(stepper)
        assert "Stepper" in text
        assert str(instance.value) in text
        assert str(stepper.step) in text