"""
Tests for `find_longest_keys(path_dict)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_constants.utils import (
    find_longest_keys,
)


class TestFindLongestKeys:

    def test_single_entry_returns_itself(self):
        path_dict = {"a": ("a",)}
        assert find_longest_keys(path_dict) == ("a",)

    def test_flat_independent_paths_all_terminal(self):
        path_dict = {
            "a": ("a",),
            "b": ("b",),
            "c": ("c",),
        }
        result = find_longest_keys(path_dict)
        assert set(result) == {"a", "b", "c"}

    def test_intermediate_path_is_excluded(self):
        """
        'pair' is a prefix of 'first' (pair -> pair.first), so 'pair'
        must NOT be included in the result, only 'first'.
        """
        path_dict = {
            "pair": ("pair",),
            "first": ("pair", "first"),
        }
        result = find_longest_keys(path_dict)
        assert "first" in result
        assert "pair" not in result

    def test_mixed_nested_and_flat(self):
        path_dict = {
            "outer": ("outer",),
            "pair": ("outer", "pair"),
            "first": ("outer", "pair", "first"),
            "third": ("outer", "third"),
        }
        result = find_longest_keys(path_dict)
        assert set(result) == {"first", "third"}