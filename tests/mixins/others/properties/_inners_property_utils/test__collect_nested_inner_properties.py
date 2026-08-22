"""
Tests for `_collect_nested_inner_properties(meta, path, result)`.
"""
from simplibs.object.mixins.others.properties._inners_property_utils._collect_nested_inner_properties import (
    _collect_nested_inner_properties,
)


class TestCollectNestedInnerProperties:

    def test_mutates_result_dict_in_place(self, Outer):
        pair_meta = next(
            inner.meta for inner in Outer.meta.inners
            if inner.meta.name_snake == "pair"
        )
        result = {}
        _collect_nested_inner_properties(pair_meta, ("_pair",), result)

        assert len(result) == 4
        assert "first" in result
        assert "first_instance" in result
        assert "second" in result
        assert "second_instance" in result

    def test_all_collected_are_properties(self, Outer):
        pair_meta = next(
            inner.meta for inner in Outer.meta.inners
            if inner.meta.name_snake == "pair"
        )
        result = {}
        _collect_nested_inner_properties(pair_meta, ("_pair",), result)
        assert all(isinstance(v, property) for v in result.values())

    def test_deeper_nesting_produces_more_entries(self, tree_classes):
        from simplibs.object import SimpleObject
        Outer, Pair, First, Second, Third = tree_classes

        class Wrapper(SimpleObject):
            _type = int
            _inners = (Outer,)

            @classmethod
            def _logic(cls, outer):
                return outer

        outer_meta = Wrapper.meta.inners[0].meta
        result = {}
        _collect_nested_inner_properties(outer_meta, ("_outer",), result)

        assert len(result) >= 6