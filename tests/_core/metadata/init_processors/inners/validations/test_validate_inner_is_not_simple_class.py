import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_inner_is_not_simple_class import (
    validate_inner_is_not_simple_class,
)
from simplibs.object.exceptions import SimpleDefinitionError
from simplibs.object import SimpleConstant, SimpleObject


def test_validate_inner_is_not_simple_class_pass() -> None:
    """Test that concrete subclasses pass validation."""

    dummy_owner = Mock(__name__="OwnerClass")

    class ConcreteConstant(SimpleConstant):
        _type = int
        _default = 1

    validate_inner_is_not_simple_class(ConcreteConstant, dummy_owner)


@pytest.mark.parametrize("base_class", [SimpleConstant, SimpleObject])
def test_validate_inner_is_not_simple_class_raises_error(subtests, base_class: type) -> None:
    """Test that referencing base classes directly raises SimpleDefinitionError."""

    dummy_owner = Mock(__name__="OwnerClass")

    assert_exception_function(
        subtests,
        validate_inner_is_not_simple_class,

        invalid_params=(base_class, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="inner_is_base_class",
        expected="Concrete subclass of SimpleConstant or SimpleObject",
        value=base_class,
        problem=f"Class 'OwnerClass' declares base class '{base_class.__name__}' inside _inners.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Use concrete subclasses, not the base framework classes.",
            "SimpleObject and SimpleConstant serve only as inheritance roots.",
            "Replace this reference with a specific subclass representing actual data.",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=TypeError,

        verbose=False,
    )