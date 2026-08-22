"""
Tests for `testing/asserts/mixins/assert_mixin_instance_creation.py`.
"""
import pytest
from simplibs.object.testing.asserts.mixins.assert_mixin_instance_creation import (
    assert_mixin_instance_creation,
)


class TestAssertMixinInstanceCreationHappyPath:

    def test_returns_instance_with_injected_mixin_members(self, IntConst, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        instance = assert_mixin_instance_creation(subtests, TestMixin, IntConst)

        assert instance is not None
        assert instance.test_property == "test_value"

    def test_creates_mutable_instance_by_default(self, IntConst, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        instance = assert_mixin_instance_creation(subtests, TestMixin, IntConst)

        assert instance is not None
        assert instance._is_mutable is True

    def test_creates_immutable_instance_when_mutable_is_false(self, IntConst, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        instance = assert_mixin_instance_creation(
            subtests,
            TestMixin,
            IntConst,
            mutable=False,
        )

        assert instance is not None
        assert instance._is_mutable is False


class TestAssertMixinInstanceCreationInvalidTestClass:

    def test_fails_when_test_class_does_not_inherit_simple_constant(self, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        class NotSimple:
            pass

        with pytest.raises(pytest.fail.Exception, match="must inherit from SimpleConstant"):
            assert_mixin_instance_creation(
                subtests,
                TestMixin,
                NotSimple,  # type: ignore[arg-type]
                verbose=False,
            )


class TestAssertMixinInstanceCreationInvalidMixinClass:

    def test_fails_when_mixin_does_not_inherit_simple_mixin(self, IntConst, subtests):
        class NotAMixin:
            pass

        with pytest.raises(pytest.fail.Exception, match="does not inherit from SimpleMixin"):
            assert_mixin_instance_creation(
                subtests,
                NotAMixin,  # type: ignore[arg-type]
                IntConst,
                verbose=False,
            )