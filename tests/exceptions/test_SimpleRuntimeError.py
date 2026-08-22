"""
Tests for `exceptions/SimpleRuntimeError.py`.
"""
import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleRuntimeError import SimpleRuntimeError


def test_simple_runtime_error_class(subtests) -> None:
    """Verify that SimpleRuntimeError meets all structural and behavioral exception rules."""
    assert_exception_class(
        subtests,
        SimpleRuntimeError,
        verbose=False,
    )