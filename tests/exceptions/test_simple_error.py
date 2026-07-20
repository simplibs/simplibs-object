import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleError import SimpleError


def test_simple_error_class(subtests) -> None:
    """Verify that SimpleError meets all structural and behavior exception rules."""
    assert_exception_class(
        subtests,
        SimpleError,
        verbose=False
    )
