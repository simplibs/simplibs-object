"""
Tests for `exceptions/base_exception/SimpleObjectError.py`.
"""
import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.base_exception.SimpleObjectError import SimpleObjectError


def test_simple_object_error_class(subtests) -> None:
    """Verify that SimpleObjectError meets all structural and behavioral exception rules."""
    assert_exception_class(
        subtests,
        SimpleObjectError,
        verbose=False,
    )