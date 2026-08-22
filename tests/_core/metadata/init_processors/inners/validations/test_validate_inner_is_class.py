import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_inner_is_class import (
    validate_inner_is_class,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_inner_is_class_pass() -> None:
    """Test that a valid class passes validation."""

    dummy_owner = Mock(__name__="OwnerClass")

    class InnerClass:
        pass

    validate_inner_is_class(InnerClass, (InnerClass,), dummy_owner)


@pytest.mark.parametrize(
    "invalid_inner",
    [
        "not_a_class",
        42,
        object(),
    ],
)
def test_validate_inner_is_class_raises_error(subtests, invalid_inner: object) -> None:
    """Test that non-class inner elements raise SimpleDefinitionError."""

    dummy_owner = Mock(__name__="OwnerClass")
    inners = (invalid_inner,)

    assert_exception_function(
        subtests,
        validate_inner_is_class,

        invalid_params=(invalid_inner, inners, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="inner_not_class",
        expected="Class inheriting from SimpleConstant or SimpleObject",
        value=invalid_inner,
        problem=f"Inner element '{invalid_inner}' inside '{inners}' is not a class.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Use class references, not instances.",
            "Example: MyElement, not MyElement().",
            "Ensure the item is not a string or primitive value.",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=TypeError,

        verbose=False,
    )