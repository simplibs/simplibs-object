"""
Tests for `FORBIDDEN_NAMES` constant set.
"""
from simplibs.object.mixins._common_logic.constants.sets import FORBIDDEN_NAMES


class TestForbiddenNamesContent:
    """Verifies the exact contents of the forbidden names set for mixin __slots__ / namespace."""

    EXPECTED = {
        "__init__",
        "__metadata__",
        "_decompose",
        "_inners",
        "_logic",
        "_owner",
        "_recalculate_inners",
        "_recalculate_self",
        "_value",
        "meta",
        "owner",
        "value",
    }

    def test_is_set(self):
        assert isinstance(FORBIDDEN_NAMES, set)

    def test_exact_content(self):
        assert FORBIDDEN_NAMES == self.EXPECTED

    def test_contains_core_identity_names(self):
        # Sanity check for critical entries to verify core semantics
        assert "value" in FORBIDDEN_NAMES
        assert "meta" in FORBIDDEN_NAMES
        assert "_value" in FORBIDDEN_NAMES
        assert "__init__" in FORBIDDEN_NAMES