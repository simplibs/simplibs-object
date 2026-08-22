"""
Tests for `PickleReduce` mixin.
"""
import pickle
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.mixins.dunders.lifecycles import PickleReduce, PickleState
from simplibs.object.mixins.dunders.lifecycles._utils.rebuild_simple_instance import (
    rebuild_simple_instance,
)
from simplibs.object.testing import assert_simple_mixin


# ---------------------------------------------------------------------------
# Module-level classes for pickle compatibility
# ---------------------------------------------------------------------------

class PickleLeaf(SimpleConstant):
    _type = int
    _default = 10


class PickleComposite(SimpleObject):
    _type = int
    _inners = (PickleLeaf,)

    @classmethod
    def _logic(cls, pickle_leaf):
        return pickle_leaf

    @classmethod
    def _decompose(cls, value):
        return (value,)


# ---------------------------------------------------------------------------
# Test Suites
# ---------------------------------------------------------------------------

class TestPickleReduceStructure:

    def test_inherits_from_pickle_state(self):
        assert issubclass(PickleReduce, PickleState)

    def test_slots_empty(self):
        assert PickleReduce.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            PickleReduce,
            test_class=Outer,
            method_names=("__reduce__",),
        )


class TestPickleReduceContent:

    def test_reduce_returns_two_tuple(self, Outer):
        instance = Outer(mixins=(PickleReduce,))
        result = instance.__reduce__()
        assert len(result) == 2

    def test_reduce_first_element_is_rebuild_helper(self, Outer):
        instance = Outer(mixins=(PickleReduce,))
        callable_, _ = instance.__reduce__()
        assert callable_ is rebuild_simple_instance

    def test_reduce_second_element_contains_expected_arguments(self, Outer):
        instance = Outer(mixins=(PickleReduce,), mutable=True)
        _, args = instance.__reduce__()

        assert len(args) == 5
        owner_class, mixins, is_constant, is_mutable, state = args

        assert owner_class is instance.meta.owner_class
        assert PickleReduce in mixins
        assert is_constant == instance.__is_constant__
        assert is_mutable is True
        assert state == instance.__getstate__()


class TestPickleReduceRoundTrip:

    def test_full_pickle_unpickle_round_trip_mutable(self):
        instance = PickleComposite(mixins=(PickleReduce,), mutable=True)
        instance.value = 500

        pickled = pickle.dumps(instance)
        restored = pickle.loads(pickled)

        assert restored.value == 500
        assert restored.__is_mutable__ is True
        assert isinstance(restored, PickleReduce)

    def test_full_pickle_unpickle_round_trip_immutable(self):
        instance = PickleComposite(mixins=(PickleReduce,), mutable=False)

        pickled = pickle.dumps(instance)
        restored = pickle.loads(pickled)

        assert restored.value == instance.value
        assert restored.__is_mutable__ is False
        assert isinstance(restored, PickleReduce)