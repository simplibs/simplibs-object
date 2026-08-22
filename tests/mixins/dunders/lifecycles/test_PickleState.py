"""
Tests for `PickleState` mixin.
"""
import pytest
from simplibs.object.mixins.core_mixins import Serialization
from simplibs.object.mixins.dunders.lifecycles import PickleState
from simplibs.object.testing import assert_simple_mixin


class TestPickleStateStructure:

    def test_inherits_from_serialization(self):
        assert issubclass(PickleState, Serialization)

    def test_slots_empty(self):
        assert PickleState.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            PickleState,
            test_class=Outer,
            method_names=("__getstate__", "__setstate__"),
        )


class TestPickleStateGetState:

    def test_getstate_matches_to_dict(self, Outer):
        instance = Outer(mixins=(PickleState,))
        assert instance.__getstate__() == instance.to_dict()


class TestPickleStateSetState:

    def test_setstate_mutable_updates_in_place(self, Outer):
        instance = Outer(mixins=(PickleState,), mutable=True)
        state = instance.to_dict()
        state["third"] = 55

        instance.__setstate__(state)

        assert instance._nodes_dict["third"][0].value == 55

    def test_setstate_requires_from_dict_method(self, Outer):
        instance = Outer(mixins=(PickleState,), mutable=True)
        assert hasattr(instance.__class__, "from_dict")