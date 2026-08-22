"""
Tests for `testing/containers/MixinCase.py`.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.object.testing.containers.MixinCase import MixinCase
from simplibs.object.testing.containers.TestMixin import TestMixin


class TestMixinCaseDefaults:

    def test_optional_fields_default_to_unset(self, IntConst):
        case = MixinCase(mixin_class=TestMixin, test_class=IntConst)

        assert case.slots_names is UNSET
        assert case.slots_values is UNSET
        assert case.attribute_names is UNSET
        assert case.method_names is UNSET

    def test_is_keyword_only(self, IntConst):
        with pytest.raises(TypeError):
            MixinCase(TestMixin, IntConst)


class TestMixinCaseRunTest:

    def test_run_test_returns_instance_with_mixin_applied(self, IntConst, subtests):
        case = MixinCase(mixin_class=TestMixin, test_class=IntConst)
        instance = case.run_test(subtests)

        assert instance is not None
        assert hasattr(instance, "test_method")
        assert hasattr(instance, "_test_slot")

    def test_run_test_forwards_slots_values_check(self, IntConst, subtests):
        case = MixinCase(
            mixin_class=TestMixin,
            test_class=IntConst,
            slots_values=("_test_slot", "test_value"),
        )
        instance = case.run_test(subtests)
        assert instance is not None
        assert instance._test_slot == "test_value"

    def test_run_test_forwards_method_names_check(self, IntConst, subtests):
        case = MixinCase(
            mixin_class=TestMixin,
            test_class=IntConst,
            method_names=("test_method",),
        )
        instance = case.run_test(subtests)
        assert instance is not None
        assert callable(instance.test_method)