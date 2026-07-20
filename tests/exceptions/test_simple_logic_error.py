import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleLogicError import SimpleLogicError


def test_simple_logic_error_class(subtests) -> None:
    """Verify that SimpleLogicError meets all structural and behavior exception rules."""
    assert_exception_class(
        subtests,
        SimpleLogicError,
        verbose=False
    )