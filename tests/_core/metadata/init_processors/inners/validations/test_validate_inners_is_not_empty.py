import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_inners_is_not_empty import (
    validate_inners_is_not_empty,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_inners_is_not_empty_pass() -> None:
    """Test that non-empty tuple or non-tuple values pass through this specific validator."""

    dummy_owner = Mock(__name__="OwnerClass")

    validate_inners_is_not_empty(("ElementA",), dummy_owner)


def test_validate_inners_is_not_empty_raises_error(subtests) -> None:
    """Test that empty tuple raises SimpleDefinitionError."""

    dummy_owner = Mock(__name__="OwnerClass")
    empty_tuple = ()

    assert_exception_function(
        subtests,
        validate_inners_is_not_empty,

        invalid_params=(empty_tuple, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="_inners_empty",
        expected="Non-empty tuple of SimpleConstant / SimpleObject subclasses",
        value=empty_tuple,
        problem="Class 'OwnerClass' defines '_inners' as an empty tuple.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Remove '_inners' entirely if the class has no inner components.",
            "If this is a composition, define at least one inner element.",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=ValueError,

        verbose=False,
    )