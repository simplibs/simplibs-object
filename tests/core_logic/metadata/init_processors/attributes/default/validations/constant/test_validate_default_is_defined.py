import pytest
from simplibs.sentinels import UNSET

from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.init_processors.attributes.default.validations.constant.validate_default_is_defined import (
    validate_default_is_defined,
)
from simplibs.exception.testing import (
    assert_exception_function,
    assert_function_valid_input,
)


# Mock classes mimicking metadata architecture for the exception helper
class MockSimpleObject:
    __mro__ = ("MockSimpleObject", "SimpleObject", "object")


class MockSimpleConstant:
    __mro__ = ("MockSimpleConstant", "SimpleConstant", "object")


@pytest.mark.parametrize(
    "valid_value, mock_class",
    [
        ("StandardString", MockSimpleObject),
        (100, MockSimpleConstant),
        (None, MockSimpleObject),
        (False, MockSimpleConstant),
    ],
    ids=["string_payload", "integer_payload", "none_payload", "boolean_payload"]
)
def test_validate_default_is_defined_happy_path(subtests, valid_value, mock_class) -> None:
    """Verify that any valid concrete default value passes the definition guard without exceptions."""
    assert_function_valid_input(
        subtests,
        validate_default_is_defined,
        valid_params=(valid_value, mock_class),
        verbose=False
    )


@pytest.mark.parametrize(
    "mock_class",
    [
        MockSimpleObject,
        MockSimpleConstant,
    ],
    ids=["target_class_derived_from_simple_object", "target_class_derived_from_simple_constant"]
)
def test_validate_default_is_defined_throws_on_unset(subtests, mock_class) -> None:
    """Verify that an UNSET value triggers a structured SimpleMetadataError tailored to the class type."""
    assert_exception_function(
        subtests,
        validate_default_is_defined,
        invalid_params=(UNSET, mock_class),
        exception_type=SimpleMetadataError,
        label="Attribute '_default' is not defined",
        expected="The '_default' attribute must contain a concrete default value for the constant.",
        problem="The required '_default' attribute is missing from the class definition.",
        context="Metadata evaluation and validation for:",
        how_to_fix=(
            "A constant leaf structure (SimpleConstant) must explicitly declare a '_default' value.",
            "Add the '_default = <value>' attribute directly to the body of your class definition.",
            "If this object was intended to be a structured compound entity instead, add an '_inners' mapping and a '_logic' method.",
            "Verify that the default value expression was not accidentally stripped or removed during runtime modification.",
        ),
        exception=ValueError
    )