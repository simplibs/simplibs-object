"""
Tests for `ImmutableWithInners` mixin.
"""
import pytest
from simplibs.object.mixins.others.immutable import ImmutableMethods, ImmutableWithInners


class TestImmutableWithInnersStructure:

    def test_immutable_only_flag(self):
        assert ImmutableWithInners._immutable_only is True

    def test_composite_only_flag(self):
        assert ImmutableWithInners._composite_only is True

    def test_inherits_from_immutable_methods(self):
        assert issubclass(ImmutableWithInners, ImmutableMethods)

    def test_slots_empty(self):
        assert ImmutableWithInners.__slots__ == ()

    def test_shallow_structure_manual(self, Outer):
        instance = Outer(mixins=(ImmutableWithInners,), mutable=False)
        assert isinstance(instance, ImmutableWithInners)
        assert isinstance(instance, ImmutableMethods)
        assert ImmutableWithInners in instance.__mixins__


class TestImmutableWithInnersDynamicMethods:

    def test_with_methods_generated_for_all_nodes(self, Outer):
        instance = Outer(mixins=(ImmutableWithInners,), mutable=False)
        for name in Outer.meta.node_names_set:
            assert hasattr(instance, f"with_{name}")
            assert callable(getattr(instance, f"with_{name}"))

    def test_with_method_for_constant_returns_new_instance(self, Outer):
        instance = Outer(mixins=(ImmutableWithInners,), mutable=False)
        result = instance.with_third(88)
        assert result is not instance
        assert result._nodes_dict["third"][0].value == 88

    def test_with_method_for_composite_returns_new_instance(self, Outer):
        instance = Outer(mixins=(ImmutableWithInners,), mutable=False)
        result = instance.with_pair(15)
        assert result._nodes_dict["pair"][0].value == 15

    def test_each_generated_method_closes_over_own_name(self, Outer):
        instance = Outer(mixins=(ImmutableWithInners,), mutable=False)
        result_first = instance.with_first(500)
        result_third = instance.with_third(500)

        assert result_first._nodes_dict["first"][0].value == 500
        assert result_first._nodes_dict["third"][0].value != 500

        assert result_third._nodes_dict["third"][0].value == 500
        assert result_third._nodes_dict["first"][0].value != 500


class TestImmutableWithInnersCompatibility:

    def test_rejects_mutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(ImmutableWithInners,), mutable=True)

    def test_rejects_atom_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(ImmutableWithInners,), as_atom=True, mutable=False)