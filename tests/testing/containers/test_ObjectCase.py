"""
Tests for `testing/containers/ObjectCase.py`.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.object.testing.containers.ObjectCase import ObjectCase


class TestObjectCaseDefaults:

    def test_optional_fields_default_to_unset(self, IntConst):
        case = ObjectCase(test_class=IntConst)

        assert case.mixins is UNSET
        assert case.test_value_change is UNSET
        assert case.test_reactivity_up is UNSET
        assert case.test_reactivity_down is UNSET
        assert case.test_mutability is UNSET
        assert case.test_immutability is UNSET

    def test_is_keyword_only(self, IntConst):
        with pytest.raises(TypeError):
            ObjectCase(IntConst)


class TestObjectCaseRunTest:

    def test_run_test_returns_instance(self, IntConst, subtests):
        case = ObjectCase(test_class=IntConst)
        instance = case.run_test(subtests, deep_check=False)
        assert instance is not None
        assert instance.value == IntConst.meta.default

    def test_run_test_forwards_value_change(self, IntConst, subtests):
        case = ObjectCase(test_class=IntConst, test_value_change=42)
        instance = case.run_test(subtests, deep_check=False)
        assert instance.value == 42

    def test_run_test_forwards_mutability_check(self, IntConst, subtests):
        case = ObjectCase(test_class=IntConst, test_mutability=7)
        case.run_test(subtests, deep_check=False)

    def test_run_test_forwards_immutability_check(self, IntConst, subtests):
        case = ObjectCase(test_class=IntConst, test_immutability=7)
        case.run_test(subtests, deep_check=False)