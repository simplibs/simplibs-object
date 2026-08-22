import pytest
from unittest.mock import Mock

from simplibs.sentinels import UNSET
from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.default.validations.validate_default_is_defined import (
    validate_default_is_defined,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_default_is_defined_pass() -> None:
    """Test that valid default values do not trigger any exception."""

    dummy_class = Mock(__name__="MyConstant", __mro__=("MyConstant", "SimpleConstant", "object"))

    # None je platná hodnota (není UNSET), nemělo by nic vyvolat
    validate_default_is_defined(None, dummy_class)
    validate_default_is_defined(42, dummy_class)


def test_validate_default_is_defined_raises_on_unset(subtests) -> None:
    """Test that UNSET default_value raises SimpleDefinitionError."""

    dummy_class = Mock(__name__="MyConstant", __mro__=("MyConstant", "SimpleConstant", "object"))

    assert_exception_function(
        subtests,
        validate_default_is_defined,

        invalid_params=(UNSET, dummy_class),
        exception_type=SimpleDefinitionError,

        error_name="INVALID DEFAULT DEFINITION",
        label="_default",
        value=UNSET,
        problem="The '_default' attribute is missing.",
        expected="A concrete default value.",
        how_to_fix=(
            "Define '_default' inside the class body.",
            "Constants must always declare a default value.",
            "If this class is meant to be a composite, define '_inners' instead.",
        ),
        context="Metadata validation for: MyConstant._default",
        exception=ValueError,

        verbose=False,
    )