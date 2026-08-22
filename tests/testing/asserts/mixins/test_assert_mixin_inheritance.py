"""
Tests for `testing/asserts/mixins/assert_mixin_inheritance.py`.
"""
import pytest
from simplibs.object.testing.asserts.mixins.assert_mixin_inheritance import (
    assert_mixin_inheritance,
)


class TestAssertMixinInheritanceHappyPath:

    def test_passes_for_valid_mixin(self, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        assert_mixin_inheritance(subtests, TestMixin)

    def test_passes_for_freshly_defined_mixin_subclass(self, subtests):
        from simplibs.object.mixins.base_class import SimpleMixin

        class MyMixin(SimpleMixin):
            __slots__ = ()

        assert_mixin_inheritance(subtests, MyMixin)


class TestAssertMixinInheritanceNotAClass:

    def test_fails_for_non_class_value(self, subtests):
        with pytest.raises(pytest.fail.Exception, match="is not a class"):
            assert_mixin_inheritance(
                subtests,
                "not-a-class",  # type: ignore[arg-type]
                verbose=False,
            )

    def test_fails_for_instance_instead_of_class(self, subtests):
        with pytest.raises(pytest.fail.Exception, match="is not a class"):
            assert_mixin_inheritance(
                subtests,
                object(),  # type: ignore[arg-type]
                verbose=False,
            )


class TestAssertMixinInheritanceWrongBase:

    def test_fails_for_class_not_inheriting_simple_mixin(self, subtests):
        class NotAMixin:
            pass

        with pytest.raises(pytest.fail.Exception, match="does not inherit from SimpleMixin"):
            assert_mixin_inheritance(
                subtests,
                NotAMixin,  # type: ignore[arg-type]
                verbose=False,
            )