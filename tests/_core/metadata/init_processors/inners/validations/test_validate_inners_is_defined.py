import pytest
from unittest.mock import Mock

from simplibs.sentinels import UNSET
from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_inners_is_defined import (
    validate_inners_is_defined,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_inners_is_defined_pass() -> None:
    """Test that explicitly defined _inners value passes validation."""

    dummy_owner = Mock(__name__="OwnerClass")

    validate_inners_is_defined((), dummy_owner)
    validate_inners_is_defined(("ElementA",), dummy_owner)


def test_validate_inners_is_defined_raises_error(subtests) -> None:
    """Test that UNSET _inners raises SimpleDefinitionError."""

    dummy_owner = Mock(__name__="OwnerClass")

    assert_exception_function(
        subtests,
        validate_inners_is_defined,

        invalid_params=(UNSET, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="_inners_missing",
        expected="Explicit '_inners' tuple",
        value=UNSET,
        problem="Class 'OwnerClass' does not define '_inners'.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Define '_inners' inside class 'OwnerClass'.",
            "Example:",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=AttributeError,

        verbose=False,
    )