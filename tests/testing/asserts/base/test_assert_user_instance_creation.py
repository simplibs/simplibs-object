"""
Tests for `testing/asserts/base/assert_user_instance_creation.py`.
"""
import pytest
from simplibs.object.testing.asserts.base.assert_user_instance_creation import (
    assert_user_instance_creation,
)


class TestAssertUserInstanceCreationVanilla:

    def test_default_unset_mixins_creates_plain_instance(self, IntConst, subtests):
        instance = assert_user_instance_creation(subtests, IntConst)
        assert instance is not None
        assert instance.value == IntConst.meta.default

    def test_explicit_empty_tuple_mixins(self, IntConst, subtests):
        instance = assert_user_instance_creation(subtests, IntConst, mixins=())
        assert instance is not None


class TestAssertUserInstanceCreationWithMixins:

    def test_creates_instance_with_provided_mixins(self, IntConst, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        instance = assert_user_instance_creation(subtests, IntConst, mixins=(TestMixin,))
        assert instance.test_property == "test_value"


class TestAssertUserInstanceCreationInvalidMixinsType:

    def test_non_tuple_mixins_fails(self, IntConst, subtests):
        with pytest.raises(pytest.fail.Exception, match="Parameter 'mixins' must be a tuple"):
            assert_user_instance_creation(
                subtests,
                IntConst,
                mixins=[],
                verbose=False,
            )


class TestAssertUserInstanceCreationDoesNotCheckMixinPropagation:

    def test_returns_instance_without_deep_structural_checks(self, IntConst, subtests):
        instance = assert_user_instance_creation(subtests, IntConst)
        assert not hasattr(instance, "test_property")