import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleInstanceError import SimpleInstanceError


def test_simple_instance_error_class(subtests) -> None:
    """Verify that SimpleInstanceError meets all structural and behavior exception rules."""
    assert_exception_class(
        subtests,
        SimpleInstanceError,
        verbose=False
    )