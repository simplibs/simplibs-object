"""
Tests for `from_dict_constants(self, user_dict)`.
"""
import pytest
from simplibs.object.mixins.core_mixins import Infrastructure
from simplibs.object.mixins.core_mixins._utils.serialization import from_dict_constants


class TestFromDictConstantsMutable:

    def test_updates_matching_constants_in_place(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        result = from_dict_constants(instance, {"first": 100})
        assert result is instance
        assert instance._nodes_dict["first"][0].value == 100

    def test_partial_dict_only_updates_present_keys(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        original_second = instance._nodes_dict["second"][0].value
        from_dict_constants(instance, {"first": 100})
        assert instance._nodes_dict["second"][0].value == original_second

    def test_no_matching_keys_returns_self_unchanged(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        original_value = instance.value
        result = from_dict_constants(instance, {"completely_unrelated_key": 1})
        assert result is instance
        assert instance.value == original_value


class TestFromDictConstantsImmutable:

    def test_returns_new_instance_with_changes(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=False)
        result = from_dict_constants(instance, {"first": 100})
        assert result is not instance
        assert result._nodes_dict["first"][0].value == 100

    def test_no_changes_returns_self(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=False)
        result = from_dict_constants(instance, {"completely_unrelated_key": 1})
        assert result is instance

    def test_original_unchanged_after_immutable_update(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=False)
        original_value = instance.value
        from_dict_constants(instance, {"third": 999})
        assert instance.value == original_value


class TestFromDictConstantsValidation:

    def test_non_dict_input_raises(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        with pytest.raises(Exception):
            from_dict_constants(instance, "not_a_dict")