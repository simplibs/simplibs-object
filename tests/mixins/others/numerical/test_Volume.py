"""
Tests for `Volume` mixin.
"""
import pytest
from numbers import Number
from simplibs.object.mixins.others.numerical import Volume
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.testing import assert_simple_mixin


class TestVolumeStructure:

    def test_mutable_only_flag(self):
        assert Volume._mutable_only is True

    def test_only_types_is_number(self):
        assert Volume._only_types is Number

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Volume,
            test_class=IntLeaf,
            slots_names=("_value_stepper",),
            attribute_names=("value_stepper",),
        )


class TestVolumeBehavior:

    def test_value_stepper_is_stepper_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Volume,), as_atom=True, mutable=True)
        assert isinstance(instance.value_stepper, Stepper)

    def test_value_stepper_bound_to_self(self, IntLeaf):
        instance = IntLeaf(mixins=(Volume,), as_atom=True, mutable=True)
        assert instance.value_stepper._instance is instance

    def test_step_up_via_stepper_modifies_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Volume,), as_atom=True, mutable=True)
        original = instance.value
        instance.value_stepper.step_up()
        assert instance.value == original + 1


class TestVolumeCompatibility:

    def test_rejects_immutable_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(Volume,), as_atom=True, mutable=False)

    def test_rejects_non_numeric_type(self):
        from simplibs.object import SimpleConstant

        class StrLeaf(SimpleConstant):
            _type = str
            _default = "x"

        with pytest.raises(Exception):
            StrLeaf(mixins=(Volume,), as_atom=True, mutable=True)