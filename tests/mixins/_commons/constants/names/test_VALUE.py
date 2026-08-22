"""
Tests for `VALUE` constant name.
"""
from simplibs.object.mixins._common_logic.constants.names import VALUE


def test_value_value():
    assert VALUE == "_value"


def test_value_is_str():
    assert isinstance(VALUE, str)