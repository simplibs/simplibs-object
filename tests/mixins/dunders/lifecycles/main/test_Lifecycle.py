"""
Tests for `Lifecycle` bundle mixin - `Copyable + PickleReduce`.
"""
import copy
import pickle
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.mixins.dunders.lifecycles import Copyable, PickleReduce
from simplibs.object.mixins.dunders.lifecycles.main import Lifecycle
from simplibs.object.testing import assert_simple_mixin


# ---------------------------------------------------------------------------
# Module-level classes for pickle compatibility
# ---------------------------------------------------------------------------

class LifecycleLeaf(SimpleConstant):
    _type = int
    _default = 10


class LifecycleComposite(SimpleObject):
    _type = int
    _inners = (LifecycleLeaf,)

    @classmethod
    def _logic(cls, lifecycle_leaf):
        return lifecycle_leaf

    @classmethod
    def _decompose(cls, value):
        return (value,)


# ---------------------------------------------------------------------------
# Test Suites
# ---------------------------------------------------------------------------

class TestLifecycleStructure:

    def test_inherits_from_copyable_and_pickle_reduce(self):
        assert issubclass(Lifecycle, Copyable)
        assert issubclass(Lifecycle, PickleReduce)

    def test_slots_empty(self):
        assert Lifecycle.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(subtests, Lifecycle, test_class=Outer)


class TestLifecycleCombinedAPI:

    def test_provides_both_copy_and_pickle_api(self):
        instance = LifecycleComposite(mixins=(Lifecycle,), mutable=True)

        copied = copy.copy(instance)
        assert copied._build_snapshot() == instance._build_snapshot()

        pickled = pickle.dumps(instance)
        restored = pickle.loads(pickled)
        assert restored.value == instance.value

    def test_no_slot_conflict_on_instantiation(self, Outer):
        instance = Outer(mixins=(Lifecycle,))
        assert instance is not None