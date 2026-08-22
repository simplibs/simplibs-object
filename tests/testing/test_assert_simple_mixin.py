"""
Tests for `testing/assert_simple_mixin.py`.
"""
from simplibs.object.testing.assert_simple_mixin import assert_simple_mixin
from simplibs.object.testing.containers.TestMixin import TestMixin


class TestAssertSimpleMixinShallowOnly:

    def test_returns_instance_with_mixin_applied(self, IntConst, subtests):
        instance = assert_simple_mixin(subtests, TestMixin, test_class=IntConst)
        assert instance is not None
        assert hasattr(instance, "test_method")
        assert instance.test_method() == "[TestMixin] property=test_value"


class TestAssertSimpleMixinAllParameterChecks:

    def test_runs_full_parameter_suite(self, IntConst, subtests):
        instance = assert_simple_mixin(
            subtests,
            TestMixin,
            test_class=IntConst,
            slots_names=("_test_slot",),
            slots_values=("_test_slot", "test_value"),
            attribute_names=("test_property",),
            method_names=("test_method", "test_class_method"),
        )
        assert instance.test_method() == "[TestMixin] property=test_value"

    def test_intro_and_verbose_do_not_affect_outcome(self, IntConst, subtests):
        instance = assert_simple_mixin(
            subtests, TestMixin, test_class=IntConst, verbose=False, intro="Suite::"
        )
        assert instance is not None