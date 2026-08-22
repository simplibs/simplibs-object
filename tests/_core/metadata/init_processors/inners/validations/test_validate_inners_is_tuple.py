import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_inners_is_tuple import (
    validate_inners_is_tuple,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_inners_is_tuple_pass() -> None:
    """Test that tuple instance passes validation."""

    dummy_owner = Mock(__name__="OwnerClass")

    validate_inners_is_tuple((), dummy_owner)
    validate_inners_is_tuple(("ElementA", "ElementB"), dummy_owner)


@pytest.mark.parametrize(
    "invalid_inners",
    [
        ["ElementA"],
        {"ElementA"},
        "ElementA",
        123,
    ],
)
def test_validate_inners_is_tuple_raises_error(subtests, invalid_inners: object) -> None:
    """Test that non-tuple values raise SimpleDefinitionError."""

    dummy_owner = Mock(__name__="OwnerClass")

    assert_exception_function(
        subtests,
        validate_inners_is_tuple,

        invalid_params=(invalid_inners, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="_inners_not_tuple",
        expected="Tuple of SimpleConstant / SimpleObject subclasses",
        value=invalid_inners,
        problem="Class 'OwnerClass' defines '_inners' using an invalid type.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Define '_inners' as a tuple.",
            "Example: _inners = (ElementA, ElementB)",
            "Single element requires a trailing comma: (ElementA,)",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=TypeError,

        verbose=False,
    )