"""
Tests for `from_dict(self, user_dict)`.
"""
import pytest
from simplibs.object.mixins._common_logic.constants import OWNER_CLASS
from simplibs.object.mixins.core_mixins import Infrastructure
from simplibs.object.mixins.core_mixins._utils.serialization import from_dict, to_dict


class TestFromDictMutable:

    def test_updates_in_place_and_returns_self(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        state = to_dict(instance)
        state["pair"]["first"] = 50

        result = from_dict(instance, state)

        assert result is instance
        assert instance._nodes_dict["first"][0].value == 50

    def test_owner_class_mismatch_raises(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        bad_state = {OWNER_CLASS: "SomeOtherClass"}
        with pytest.raises(Exception):
            from_dict(instance, bad_state)

    def test_non_dict_input_raises(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        with pytest.raises(Exception):
            from_dict(instance, "not_a_dict")

    def test_missing_key_raises(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=True)
        incomplete_state = {OWNER_CLASS: instance.meta.owner_class}
        with pytest.raises(Exception):
            from_dict(instance, incomplete_state)


class TestFromDictImmutable:

    def test_returns_new_instance(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=False)
        state = to_dict(instance)
        state["third"] = 99

        result = from_dict(instance, state)

        assert result is not instance
        assert result._nodes_dict["third"][0].value == 99

    def test_original_unchanged(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=False)
        original_value = instance.value
        state = to_dict(instance)
        state["third"] = 999

        from_dict(instance, state)

        assert instance.value == original_value


class TestFromDictRoundTrip:

    def test_to_dict_from_dict_round_trip(self, Outer):
        instance = Outer(mixins=(Infrastructure,), mutable=False)
        state = to_dict(instance)
        result = from_dict(instance, state)
        assert to_dict(result) == state