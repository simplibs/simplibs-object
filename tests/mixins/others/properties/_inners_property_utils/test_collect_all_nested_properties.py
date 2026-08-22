"""
Tests for `collect_all_nested_properties(meta)`.
"""
from simplibs.object.mixins.others.properties._inners_property_utils import (
    collect_all_nested_properties,
)


class TestCollectAllNestedProperties:

    def test_returns_dict(self, Outer):
        result = collect_all_nested_properties(Outer.meta)
        assert isinstance(result, dict)

    def test_all_values_are_properties(self, Outer):
        result = collect_all_nested_properties(Outer.meta)
        assert all(isinstance(value, property) for value in result.values())

    def test_direct_inners_are_not_top_level_skipped_but_recursed(self, Outer):
        result = collect_all_nested_properties(Outer.meta)
        assert len(result) == 4
        assert "first" in result
        assert "first_instance" in result
        assert "second" in result
        assert "second_instance" in result

    def test_composite_with_only_direct_constants_has_no_nested_properties(self, tree_classes):
        _, Pair, _, _, _ = tree_classes
        result = collect_all_nested_properties(Pair.meta)
        assert result == {}

    def test_non_decomposable_deep_tree_still_collects_structurally(self, tree_classes):
        from simplibs.object import SimpleObject
        Outer, Pair, First, Second, Third = tree_classes

        class NoDecomposeOuter(SimpleObject):
            _type = int
            _inners = (Pair, Third)

            @classmethod
            def _logic(cls, pair, third):
                return pair + third

        result = collect_all_nested_properties(NoDecomposeOuter.meta)
        assert len(result) == 4
        assert "first" in result
        assert "first_instance" in result
        assert "second" in result
        assert "second_instance" in result