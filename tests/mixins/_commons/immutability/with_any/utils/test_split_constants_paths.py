"""
Tests for `split_constants_paths(constants, used_paths_dict, nodes_path_dict)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_any.utils import (
    split_constants_paths,
)


class TestSplitConstantsPaths:

    def test_constant_contained_in_used_path(self):
        constants = (("first", 10),)
        used_paths_dict = {"pair": ("outer", "pair")}
        nodes_path_dict = {"first": ("outer", "pair", "first")}

        contained, unique = split_constants_paths(
            constants, used_paths_dict, nodes_path_dict
        )

        assert "first" in contained
        assert unique == {}

    def test_constant_contained_when_composite_path_ends_with_value_sentinel(self):
        constants = (("first", 10),)
        used_paths_dict = {"pair": ("pair", "_value")}
        nodes_path_dict = {"first": ("pair", "first")}

        contained, unique = split_constants_paths(
            constants, used_paths_dict, nodes_path_dict
        )

        assert "first" in contained
        assert unique == {}

    def test_constant_not_contained_is_unique(self):
        constants = (("third", 3),)
        used_paths_dict = {"pair": ("outer", "pair")}
        nodes_path_dict = {"third": ("outer", "third")}

        contained, unique = split_constants_paths(
            constants, used_paths_dict, nodes_path_dict
        )

        assert contained == {}
        assert "third" in unique

    def test_constant_unique_when_composite_path_ends_with_value_sentinel(self):
        constants = (("third", 3),)
        used_paths_dict = {"pair": ("pair", "_value")}
        nodes_path_dict = {"third": ("third",)}

        contained, unique = split_constants_paths(
            constants, used_paths_dict, nodes_path_dict
        )

        assert contained == {}
        assert "third" in unique

    def test_mixed_contained_and_unique(self):
        constants = (("first", 10), ("third", 3))
        used_paths_dict = {"pair": ("outer", "pair", "_value")}
        nodes_path_dict = {
            "first": ("outer", "pair", "first"),
            "third": ("outer", "third"),
        }

        contained, unique = split_constants_paths(
            constants, used_paths_dict, nodes_path_dict
        )

        assert "first" in contained
        assert "third" in unique

    def test_returns_two_dicts(self):
        constants = (("first", 10),)
        used_paths_dict = {}
        nodes_path_dict = {"first": ("first",)}

        result = split_constants_paths(constants, used_paths_dict, nodes_path_dict)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(item, dict) for item in result)