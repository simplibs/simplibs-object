"""
Tests for `Equalizer` mixin.
"""
import pytest
from numbers import Number
from simplibs.object.mixins._common_logic.constants import STEPPER
from simplibs.object.mixins.core_mixins import NodesTuple
from simplibs.object.mixins.others.numerical import Equalizer
from simplibs.object.mixins.others.numerical._stepper_class import Stepper
from simplibs.object.testing import assert_simple_mixin


class TestEqualizerStructure:

    def test_composite_only_flag(self):
        assert Equalizer._composite_only is True

    def test_mutable_only_flag(self):
        assert Equalizer._mutable_only is True

    def test_only_types_is_number(self):
        assert Equalizer._only_types is Number

    def test_inherits_from_nodes_tuple(self):
        assert issubclass(Equalizer, NodesTuple)

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Equalizer,
            test_class=Outer,
            slots_names=("_steppers",),
        )


class TestEqualizerDynamicProperties:

    def test_stepper_property_generated_for_every_node(self, Outer):
        instance = Outer(mixins=(Equalizer,), mutable=True)
        for name in Outer.meta.node_names_set:
            prop_name = f"{name}{STEPPER}"
            assert hasattr(instance, prop_name)
            assert isinstance(getattr(instance, prop_name), Stepper)

    def test_each_stepper_bound_to_correct_node_instance(self, Outer):
        instance = Outer(mixins=(Equalizer,), mutable=True)
        third_stepper = getattr(instance, f"third{STEPPER}")
        assert third_stepper._instance.meta.name_snake == "third"

    def test_steppers_dict_keyed_by_name_snake(self, Outer):
        instance = Outer(mixins=(Equalizer,), mutable=True)
        assert set(instance._steppers.keys()) == set(Outer.meta.node_names_set)

    def test_stepping_one_node_does_not_affect_others(self, Outer):
        instance = Outer(mixins=(Equalizer,), mutable=True)
        original_second = instance._steppers["second"]._instance._value

        instance.third_stepper.step_up()

        assert instance._steppers["second"]._instance._value == original_second


class TestEqualizerCompatibility:

    def test_rejects_atom_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(Equalizer,), as_atom=True, mutable=True)

    def test_rejects_immutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(Equalizer,), mutable=False)