import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleMetadataError import SimpleMetadataError


def test_simple_metadata_error_class(subtests) -> None:
    """Verify that SimpleMetadataError meets all structural and behavior exception rules."""
    assert_exception_class(
        subtests,
        SimpleMetadataError,
        verbose=False
    )