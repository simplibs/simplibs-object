"""
Tests for helper factory function `rebuild_simple_instance`.
"""
import pytest
from simplibs.object.mixins.dunders.lifecycles import PickleReduce
from simplibs.object.mixins.dunders.lifecycles._utils.rebuild_simple_instance import (
    rebuild_simple_instance,
)


class TestRebuildSimpleInstance:

    def test_rebuild_creates_mutable_instance_with_state(self, Outer):
        original = Outer(mixins=(PickleReduce,), mutable=True)
        original.value = 123
        state = original.__getstate__()

        restored = rebuild_simple_instance(
            owner_class=Outer,
            mixins=(PickleReduce,),
            as_atom=False,
            mutable=True,
            state=state,
        )

        assert restored.value == 123
        assert restored.__is_mutable__ is True
        assert isinstance(restored, PickleReduce)

    def test_rebuild_creates_immutable_instance_with_state(self, Outer):
        original = Outer(mixins=(PickleReduce,), mutable=False)
        state = original.__getstate__()

        restored = rebuild_simple_instance(
            owner_class=Outer,
            mixins=(PickleReduce,),
            as_atom=False,
            mutable=False,
            state=state,
        )

        assert restored.value == original.value
        assert restored.__is_mutable__ is False
        assert isinstance(restored, PickleReduce)

    def test_rebuild_preserves_atom_topology(self, IntLeaf):
        original = IntLeaf(mixins=(PickleReduce,), as_atom=True, mutable=True)
        state = original.__getstate__()

        restored = rebuild_simple_instance(
            owner_class=IntLeaf,
            mixins=(PickleReduce,),
            as_atom=True,
            mutable=True,
            state=state,
        )

        assert restored.__is_constant__ is True
        assert isinstance(restored, PickleReduce)