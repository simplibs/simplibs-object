"""
Tests for `testing/assert_simple_object.py`.
"""
from simplibs.object.testing.assert_simple_object import assert_simple_object
from simplibs.object.testing.containers.InnerValue import InnerValue


class TestAssertSimpleObjectShallowOnly:

    def test_deep_check_false_runs_only_shallow_and_parameter_tests(self, IntConst, subtests):
        instance = assert_simple_object(subtests, IntConst, deep_check=False)
        assert instance is not None
        assert instance.value == IntConst.meta.default


class TestAssertSimpleObjectDeepCheck:

    def test_deep_check_true_runs_synthetic_mixin_test_too(self, IntConst, subtests):
        instance = assert_simple_object(subtests, IntConst)
        assert instance is not None

    def test_deep_check_skips_validate_method_when_not_overridden(self, IntConst, subtests):
        assert_simple_object(subtests, IntConst)

    def test_deep_check_runs_validate_method_when_overridden(self, PositiveIntConst, subtests):
        assert_simple_object(subtests, PositiveIntConst)


class TestAssertSimpleObjectValueChange:

    def test_value_change_parameter(self, IntConst, subtests):
        instance = assert_simple_object(
            subtests, IntConst, test_value_change=99, deep_check=False
        )
        assert instance.value == 99


class TestAssertSimpleObjectMutability:

    def test_mutability_parameter(self, IntConst, subtests):
        assert_simple_object(subtests, IntConst, test_mutability=42, deep_check=False)

    def test_immutability_parameter(self, IntConst, subtests):
        assert_simple_object(subtests, IntConst, test_immutability=42, deep_check=False)


class TestAssertSimpleObjectReactivity:

    def test_reactivity_down_parameter(self, PairObject, subtests):
        instance = assert_simple_object(
            subtests, PairObject, test_reactivity_down=7, deep_check=False
        )
        assert instance.value == 7

    def test_reactivity_up_parameter(self, NonDecomposablePairObject, subtests):
        instance = assert_simple_object(
            subtests,
            NonDecomposablePairObject,
            test_reactivity_up=InnerValue(path="first", value=123),
            deep_check=False,
        )
        assert instance.first == 123


class TestAssertSimpleObjectMixinsForwarding:

    def test_mixins_are_applied_to_user_instance(self, IntConst, subtests):
        from simplibs.object.testing.containers.TestMixin import TestMixin

        instance = assert_simple_object(
            subtests, IntConst, mixins=(TestMixin,), deep_check=False
        )
        assert instance.test_property == "test_value"