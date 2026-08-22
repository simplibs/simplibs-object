"""
Tests for `OWNER_CLASS` constant name.
"""
from simplibs.object.mixins._common_logic.constants.names import OWNER_CLASS


def test_owner_class_value():
    assert OWNER_CLASS == "_owner_class"


def test_owner_class_is_str():
    assert isinstance(OWNER_CLASS, str)