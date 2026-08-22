"""
Tests for `exceptions/SimpleInitializationError.py`.
"""
import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleInitializationError import SimpleInitializationError


def test_simple_initialization_error_class(subtests) -> None:
    """Verify that SimpleInitializationError meets all structural and behavioral exception rules."""
    assert_exception_class(
        subtests,
        SimpleInitializationError,
        verbose=False,
    )