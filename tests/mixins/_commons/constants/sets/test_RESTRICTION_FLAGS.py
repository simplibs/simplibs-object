"""
Tests for `RESTRICTION_FLAGS` constant tuple.
"""
from simplibs.object.mixins._common_logic.constants.sets import RESTRICTION_FLAGS


class TestRestrictionFlagsContent:
    """Verifies the exact contents of the declarative compatibility flags tuple."""

    EXPECTED = (
        "_constant_only",
        "_composite_only",
        "_mutable_only",
        "_immutable_only",
    )

    def test_is_tuple(self):
        assert isinstance(RESTRICTION_FLAGS, tuple)

    def test_exact_content(self):
        assert RESTRICTION_FLAGS == self.EXPECTED

    def test_all_items_are_str(self):
        assert all(isinstance(item, str) for item in RESTRICTION_FLAGS)

    def test_does_not_include_only_types(self):
        # _only_types is validated separately and does not belong to boolean RESTRICTION_FLAGS
        assert "_only_types" not in RESTRICTION_FLAGS