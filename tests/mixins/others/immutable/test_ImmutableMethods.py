"""
Tests for `ImmutableMethods` mixin.
"""
import pytest
from simplibs.object.mixins.core_mixins import Infrastructure
from simplibs.object.mixins.others.immutable import ImmutableMethods


class TestImmutableMethodsStructure:

    def test_immutable_only_flag(self):
        assert ImmutableMethods._immutable_only is True

    def test_inherits_from_infrastructure(self):
        assert issubclass(ImmutableMethods, Infrastructure)

    def test_slots_empty(self):
        assert ImmutableMethods.__slots__ == ()

    def test_methods_present_on_immutable_instance(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        for name in (
            "with_constants",
            "with_constant",
            "with_composite",
            "with_changes",
            "with_value",
            "duplicate",
        ):
            assert hasattr(instance, name)
            assert callable(getattr(instance, name))


class TestImmutableMethodsCoreAPI:

    def test_with_constant_returns_new_instance(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.with_constant("third", 50)
        assert result is not instance
        assert result._nodes_dict["third"][0].value == 50

    def test_with_composite_returns_new_instance(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.with_composite("pair", 20)
        assert result._nodes_dict["pair"][0].value == 20

    def test_with_constants_returns_new_instance(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.with_constants((("first", 5), ("third", 9)))
        assert result._nodes_dict["first"][0].value == 5
        assert result._nodes_dict["third"][0].value == 9

    def test_with_constants_default_none(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.with_constants()
        assert result.value == instance.value


class TestImmutableMethodsExtendedAPI:

    def test_with_changes_accepts_dict(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.with_changes({"third": 77})
        assert result._nodes_dict["third"][0].value == 77

    def test_with_changes_rejects_non_dict(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        with pytest.raises(Exception):
            instance.with_changes(("third", 77))

    def test_with_value_is_alias_for_with_composite_on_own_name(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.with_value(42)
        assert result.value == 42

    def test_duplicate_returns_equivalent_new_instance(self, Outer):
        instance = Outer(mixins=(ImmutableMethods,), mutable=False)
        result = instance.duplicate()
        assert result is not instance
        assert result._build_snapshot() == instance._build_snapshot()


class TestImmutableMethodsCompatibility:

    def test_rejects_mutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(ImmutableMethods,), mutable=True)