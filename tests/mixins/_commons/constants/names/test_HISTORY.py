"""
Tests for `HISTORY` constant name.
"""
from simplibs.object.mixins._common_logic.constants.names import HISTORY


def test_history_value():
    assert HISTORY == "history"


def test_history_is_str():
    assert isinstance(HISTORY, str)