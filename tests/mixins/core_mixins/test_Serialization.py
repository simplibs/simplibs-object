"""
Tests for `Serialization` mixin.
"""
import json
import pytest
from simplibs.object.mixins.core_mixins import Infrastructure, Serialization
from simplibs.object.testing import assert_simple_mixin


class TestSerializationStructure:

    def test_inherits_from_infrastructure(self):
        assert issubclass(Serialization, Infrastructure)

    def test_method_names_present(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Serialization,
            test_class=Outer,
            method_names=(
                "to_dict",
                "to_json",
                "from_dict",
                "from_json",
                "update_constants",
            ),
        )


class TestSerializationToDictToJson:

    def test_to_dict_returns_dict(self, Outer):
        instance = Outer(mixins=(Serialization,))
        assert isinstance(instance.to_dict(), dict)

    def test_to_json_returns_valid_json_string(self, Outer):
        instance = Outer(mixins=(Serialization,))
        json_str = instance.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed == instance.to_dict()

    def test_to_json_accepts_kwargs(self, Outer):
        instance = Outer(mixins=(Serialization,))
        json_str = instance.to_json(indent=2)
        assert "\n" in json_str


class TestSerializationFromDictFromJson:

    def test_from_dict_round_trip_mutable(self, Outer):
        instance = Outer(mixins=(Serialization,), mutable=True)
        state = instance.to_dict()
        state["third"] = 42
        result = instance.from_dict(state)
        assert result is instance
        assert instance._nodes_dict["third"][0].value == 42

    def test_from_json_round_trip(self, Outer):
        instance = Outer(mixins=(Serialization,), mutable=True)
        state = instance.to_dict()
        state["third"] = 77
        json_str = json.dumps(state)

        result = instance.from_json(json_str)

        assert result is instance
        assert instance._nodes_dict["third"][0].value == 77

    def test_from_dict_immutable_returns_new_instance(self, Outer):
        instance = Outer(mixins=(Serialization,), mutable=False)
        state = instance.to_dict()
        state["third"] = 100
        result = instance.from_dict(state)
        assert result is not instance
        assert result._nodes_dict["third"][0].value == 100


class TestSerializationUpdateConstants:

    def test_update_constants_mutable(self, Outer):
        instance = Outer(mixins=(Serialization,), mutable=True)
        result = instance.update_constants({"first": 55})
        assert result is instance
        assert instance._nodes_dict["first"][0].value == 55

    def test_update_constants_immutable(self, Outer):
        instance = Outer(mixins=(Serialization,), mutable=False)
        result = instance.update_constants({"first": 55})
        assert result is not instance
        assert result._nodes_dict["first"][0].value == 55

    def test_update_constants_partial(self, Outer):
        instance = Outer(mixins=(Serialization,), mutable=True)
        original_second = instance._nodes_dict["second"][0].value
        instance.update_constants({"first": 55})
        assert instance._nodes_dict["second"][0].value == original_second