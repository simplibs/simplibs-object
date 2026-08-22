"""
Tests for `get_top_composite_paths(composite, nodes_path_dict)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_any.utils import (
    get_top_composite_paths,
)


class TestGetTopCompositePaths:

    def test_single_composite_is_top(self):
        composite = (("pair", 10),)
        nodes_path_dict = {"pair": ("pair",)}

        top, child = get_top_composite_paths(composite, nodes_path_dict)

        assert "pair" in top
        assert child == {}

    def test_independent_composites_all_top(self):
        composite = (("pair", 10), ("other_pair", 20))
        nodes_path_dict = {
            "pair": ("pair",),
            "other_pair": ("other_pair",),
        }

        top, child = get_top_composite_paths(composite, nodes_path_dict)

        assert set(top.keys()) == {"pair", "other_pair"}
        assert child == {}

    def test_nested_composite_is_classified_as_child(self):
        """
        'outer' is ancestor of 'pair' (pair is nested inside outer).
        When both are in the same batch, 'pair' must end in child, 'outer' in top.
        """
        composite = (("outer", 100), ("pair", 10))
        nodes_path_dict = {
            "outer": ("outer",),
            "pair": ("outer", "pair"),
        }

        top, child = get_top_composite_paths(composite, nodes_path_dict)

        assert "outer" in top
        assert "pair" in child

    def test_returns_two_dicts(self):
        composite = (("pair", 10),)
        nodes_path_dict = {"pair": ("pair",)}

        result = get_top_composite_paths(composite, nodes_path_dict)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(item, dict) for item in result)