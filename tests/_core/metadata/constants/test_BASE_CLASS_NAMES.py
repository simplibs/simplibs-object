"""
Tests for `_core/metadata/constants/BASE_CLASS_NAMES.py`[cite: 81].

Acts as an explicit safety lock for the system root class names used across
`SimpleMeta.__new__`, `create_instance`, and `calculate_blueprint_path`[cite: 81].
"""
import pytest
from simplibs.object._core.metadata.constants.BASE_CLASS_NAMES import BASE_CLASS_NAMES


class TestBaseClassNames:

    def test_is_a_tuple(self) -> None:
        """Verify that BASE_CLASS_NAMES is an immutable tuple."""
        assert isinstance(BASE_CLASS_NAMES, tuple)

    def test_contains_exactly_expected_names(self) -> None:
        """Verify that BASE_CLASS_NAMES contains the exact required root system classes in order."""
        assert BASE_CLASS_NAMES == ("SimpleBase", "SimpleConstant", "SimpleObject")

    def test_count_matches_expected_length(self) -> None:
        """Verify the exact length to catch accidental additions or removals."""
        assert len(BASE_CLASS_NAMES) == 3

    def test_has_no_duplicates(self) -> None:
        """Verify all entries are unique."""
        assert len(BASE_CLASS_NAMES) == len(set(BASE_CLASS_NAMES))

    def test_all_entries_are_strings(self) -> None:
        """Verify all elements are string instances."""
        assert all(isinstance(name, str) for name in BASE_CLASS_NAMES)

    @pytest.mark.parametrize("class_name", ["SimpleBase", "SimpleConstant", "SimpleObject"])
    def test_membership_lookup(self, class_name: str) -> None:
        """Verify membership lookup for each required base class."""
        assert class_name in BASE_CLASS_NAMES