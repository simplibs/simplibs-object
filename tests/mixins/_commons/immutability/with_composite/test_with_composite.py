"""
Tests for `with_composite(self, name, new_value)`.
"""
import pytest
from simplibs.object.mixins._common_logic.immutability.with_composite import with_composite


class TestWithCompositeHappyPath:

    def test_returns_new_instance(self, immutable_outer_instance):
        result = with_composite(immutable_outer_instance, "pair", 20)
        assert result is not immutable_outer_instance

    def test_original_instance_unchanged(self, immutable_outer_instance):
        original_value = immutable_outer_instance.value
        with_composite(immutable_outer_instance, "pair", 20)
        assert immutable_outer_instance.value == original_value

    def test_composite_value_updated(self, immutable_outer_instance):
        result = with_composite(immutable_outer_instance, "pair", 20)
        assert result._nodes_dict["pair"][0].value == 20

    def test_inners_recalculated_via_decompose(self, immutable_outer_instance):
        """Pair._decompose(20) -> (20, 0) => first=20, second=0."""
        result = with_composite(immutable_outer_instance, "pair", 20)
        assert result._nodes_dict["first"][0].value == 20
        assert result._nodes_dict["second"][0].value == 0

    def test_owner_recalculated(self, immutable_outer_instance):
        """Outer = pair + third = 20 + 3(default) = 23."""
        result = with_composite(immutable_outer_instance, "pair", 20)
        assert result.value == 23


class TestWithCompositeDelegatesToConstant:

    def test_constant_name_delegates_to_with_constant(self, immutable_outer_instance):
        result = with_composite(immutable_outer_instance, "third", 77)
        assert result._nodes_dict["third"][0].value == 77


class TestWithCompositeValidation:

    def test_unknown_name_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_composite(immutable_outer_instance, "nonexistent", 1)

    def test_invalid_value_type_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_composite(immutable_outer_instance, "pair", "not_an_int")

    def test_non_decomposeable_composite_raises(self, tree_classes):
        from simplibs.object import SimpleObject
        from simplibs.object.mixins.core_mixins import Infrastructure

        Outer, Pair, First, Second, Third = tree_classes

        class NonDecomposablePair(SimpleObject):
            _type = int
            _inners = (First, Second)

            @classmethod
            def _logic(cls, first, second):
                return first + second

        class OuterWithNonDecomposablePair(SimpleObject):
            _type = int
            _inners = (NonDecomposablePair, Third)

            @classmethod
            def _logic(cls, non_decomposable_pair, third):
                return non_decomposable_pair + third

        instance = OuterWithNonDecomposablePair(mixins=(Infrastructure,), mutable=False)

        with pytest.raises(Exception):
            with_composite(instance, "non_decomposable_pair", 5)