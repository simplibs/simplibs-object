import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.default.validations.validate_default_matches_annotation import (
    validate_default_matches_annotation,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_default_matches_annotation_pass() -> None:
    """Test that matching default values pass type validation."""

    dummy_class = Mock(__name__="MyConstant", __mro__=("MyConstant", "SimpleConstant", "object"))

    validate_default_matches_annotation(42, int, dummy_class)
    validate_default_matches_annotation("hello", str, dummy_class)


@pytest.mark.parametrize(
    "default_value, expected_type",
    [
        ("not_an_int", int),
        (42, str),
        (3.14, int),
    ],
)
def test_validate_default_matches_annotation_fail(
    subtests, default_value: object, expected_type: type
) -> None:
    """Test that mismatched default values raise SimpleDefinitionError."""

    dummy_class = Mock(__name__="MyConstant", __mro__=("MyConstant", "SimpleConstant", "object"))

    assert_exception_function(
        subtests,
        validate_default_matches_annotation,

        invalid_params=(default_value, expected_type, dummy_class),
        exception_type=SimpleDefinitionError,

        error_name="INVALID DEFAULT DEFINITION",
        label="_default",
        value=default_value,
        problem="The default value does not match the declared type.",
        expected=f"A value of type {expected_type}.",
        how_to_fix=(
            f"Change '_default' to match {expected_type}.",
            "Or update '_type' to include the value's type.",
            "Constants require a type‑compliant default value.",
        ),
        context="Metadata validation for: MyConstant._default",
        exception=TypeError,

        verbose=False,
    )