import pytest
from simplibs.exception.testing import assert_exception_class
from simplibs.object.exceptions.SimpleMixinError import SimpleMixinError


def test_simple_mixin_error_class(subtests) -> None:
    """Verify that SimpleMixinError meets all structural and behavior exception rules."""
    assert_exception_class(
        subtests,
        SimpleMixinError,
        verbose=False
    )