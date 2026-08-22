"""
Tests for `STEPPER` constant name.
"""
from simplibs.object.mixins._common_logic.constants.names import STEPPER


def test_stepper_value():
    assert STEPPER == "_stepper"


def test_stepper_is_str():
    assert isinstance(STEPPER, str)