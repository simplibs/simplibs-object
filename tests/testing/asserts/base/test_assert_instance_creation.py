"""
Tests for `testing/asserts/base/assert_instance_creation.py`.
"""
from simplibs.object.testing.asserts.base.assert_instance_creation import (
    assert_instance_creation,
)


class TestAssertInstanceCreationHappyPath:

    def test_returns_working_instance_with_test_mixin_applied(self, IntConst, subtests):
        instance = assert_instance_creation(subtests, IntConst)

        assert instance is not None
        assert instance._test_slot == "test_value"
        assert instance.test_property == "test_value"
        assert instance.test_method() == "[TestMixin] property=test_value"

    def test_class_level_attribute_and_method_are_propagated(self, IntConst, subtests):
        instance = assert_instance_creation(subtests, IntConst)

        assert getattr(instance.__class__, "test_class_attribute", None) == "class_level_ok"
        assert instance.test_class_method() == "class_method_ok"

    def test_intro_prefix_does_not_affect_return_value(self, IntConst, subtests):
        instance = assert_instance_creation(subtests, IntConst, intro="MySuite::")
        assert instance is not None

    def test_verbose_false_still_runs_all_checks(self, IntConst, subtests):
        instance = assert_instance_creation(subtests, IntConst, verbose=False)
        assert instance.test_property == "test_value"