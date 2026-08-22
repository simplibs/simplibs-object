"""
Tests for `Permission` mixin.
"""
import pytest
from simplibs.object.mixins.others.state import Permission
from simplibs.object.testing import assert_simple_mixin


class TestPermissionStructure:

    def test_mutable_only_flag(self):
        assert Permission._mutable_only is True

    def test_slots_empty(self):
        assert Permission.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Permission,
            test_class=Outer,
            attribute_names=("is_locked",),
            method_names=("lock", "unlock"),
        )


class TestPermissionBehavior:

    def test_starts_unlocked(self, Outer):
        instance = Outer(mixins=(Permission,), mutable=True)
        assert instance.is_locked is False

    def test_lock_sets_is_locked_true(self, Outer):
        instance = Outer(mixins=(Permission,), mutable=True)
        instance.lock()
        assert instance.is_locked is True

    def test_unlock_sets_is_locked_false(self, Outer):
        instance = Outer(mixins=(Permission,), mutable=True)
        instance.lock()
        instance.unlock()
        assert instance.is_locked is False

    def test_lock_blocks_value_write(self, Outer):
        instance = Outer(mixins=(Permission,), mutable=True)
        instance.lock()
        with pytest.raises(Exception):
            instance.value = 999

    def test_unlock_restores_write_access(self, Outer):
        instance = Outer(mixins=(Permission,), mutable=True)
        instance.lock()
        instance.unlock()
        instance.value = instance.value


class TestPermissionCompatibility:

    def test_rejects_immutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(Permission,), mutable=False)