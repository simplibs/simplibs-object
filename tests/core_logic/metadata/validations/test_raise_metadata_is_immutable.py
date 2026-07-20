import pytest
# Outers
from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.validations.raise_metadata_is_immutable import (
    raise_metadata_is_immutable,
)
from simplibs.exception.testing import assert_exception_function


# Dummy class to simulate owner_class context
class DummyClass:
    __name__ = "DummyClass"


def test_raise_metadata_is_immutable(subtests) -> None:
    """Verify that the raiser terminates execution with a beautifully formatted metadata immutability error."""
    assert_exception_function(
        subtests,
        raise_metadata_is_immutable,
        invalid_params=("some_attribute", "old_value", "new_invalid_value", DummyClass),
        exception_type=SimpleMetadataError,
        value="new_invalid_value",
        label="Field already initialized",
        expected="Once initialized, metadata fields are read-only and cannot be overwritten.",
        problem="The field is already assigned and locked with value: 'old_value'.",
        context="Attempted to overwrite attribute 'some_attribute' inside metadata of class 'DummyClass'.",
        how_to_fix=(
            "Simple metadata fields are designed to be 'Write-Once'.",
            "After initialization, they become immutable and cannot be altered.",
            "Subsequent overwrites are only permitted for uninitialized slots (holding UNSET).",
            "If dynamic state preservation is required, utilize dedicated cache attributes or properties.",
        ),
        verbose=False
    )