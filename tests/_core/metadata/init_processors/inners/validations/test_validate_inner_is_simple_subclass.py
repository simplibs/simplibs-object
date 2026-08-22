import pytest
from unittest.mock import Mock

from simplibs.object.SimpleConstant import SimpleConstant
from simplibs.object.SimpleObject import SimpleObject
from simplibs.object._core.metadata.init_processors.inners.validations.validate_inner_is_simple_subclass import (
    validate_inner_is_simple_subclass,
)
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function


def test_validate_inner_is_simple_subclass_pass() -> None:
    """Test that subclasses of SimpleConstant or SimpleObject pass validation."""

    dummy_owner = Mock(__name__="OwnerClass")

    class MyConstant(SimpleConstant):
        _type = int
        _default = 0

    class MyConstant2(SimpleConstant):
        _type = str
        _default = ""

    # Testujeme přímo předání podtřídy do validační funkce
    validate_inner_is_simple_subclass(MyConstant, dummy_owner)
    validate_inner_is_simple_subclass(MyConstant2, dummy_owner)


def test_validate_inner_is_simple_subclass_raises_error(subtests) -> None:
    """Test that non-framework classes raise SimpleDefinitionError."""

    dummy_owner = Mock(__name__="OwnerClass")

    class PlainClass:
        pass

    assert_exception_function(
        subtests,
        validate_inner_is_simple_subclass,
        invalid_params=(PlainClass, dummy_owner),
        exception_type=SimpleDefinitionError,
        error_name="INVALID INNERS DEFINITION",
        label="inner_not_simple_subclass",
        expected="Subclass of SimpleConstant or SimpleObject",
        value=PlainClass,
        problem=f"Inner element '{PlainClass}' does not inherit from SimpleConstant.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Ensure the class inherits from SimpleConstant or SimpleObject.",
            "Verify the inheritance tree of the failing class.",
            "Check that you imported the correct class definition.",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=TypeError,
        verbose=False,
    )