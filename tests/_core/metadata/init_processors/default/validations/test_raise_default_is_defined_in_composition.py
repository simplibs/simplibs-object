import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.default.validations.raise_default_is_defined_in_composition import (
    raise_default_is_defined_in_composition,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_raise_default_is_defined_in_composition(subtests) -> None:
    """Test that defining '_default' in a composite raises SimpleDefinitionError."""

    dummy_class = Mock(__name__="MyComposite", __mro__=("MyComposite", "SimpleObject", "object"))

    assert_exception_function(
        subtests,
        raise_default_is_defined_in_composition,

        invalid_params=(dummy_class,),
        exception_type=SimpleDefinitionError,

        error_name="INVALID DEFAULT DEFINITION",
        label="_default",
        problem="The composite class 'MyComposite' defines '_default', which is forbidden.",
        expected="A composite class without '_default'.",
        how_to_fix=(
            "Remove '_default' from the class definition.",
            "Composite objects compute their value via '_inners' and '_logic'.",
            "If this class is meant to be a constant, remove '_inners' and '_logic'.",
        ),
        context="Metadata validation for: MyComposite._default",
        exception=TypeError,

        verbose=False,
    )