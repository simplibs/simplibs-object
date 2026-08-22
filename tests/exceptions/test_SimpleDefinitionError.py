"""
Tests for `exceptions/SimpleDefinitionError.py`.
"""
import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError


def test_simple_definition_error_class(subtests) -> None:
    """Verify that SimpleDefinitionError meets all structural and behavioral exception rules."""
    assert_exception_class(
        subtests,
        SimpleDefinitionError,
        verbose=False,
    )