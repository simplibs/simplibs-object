import pytest
# Outers
from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.validations.raise_attribut_allready_set import (
    raise_attribut_allready_set,
)
from simplibs.exception.testing import assert_exception_function


# Dummy class simulating the metaclass instance context
class DummyBlueprint:
    __name__ = "DummyBlueprint"
    locked_attribute = "active_configuration"


def test_raise_attribute_already_set(subtests) -> None:
    """Verify that the raiser stops execution with a precise class attribute immutability error layout."""
    assert_exception_function(
        subtests,
        raise_attribut_allready_set,
        invalid_params=(DummyBlueprint, "locked_attribute", "new_illegal_configuration"),
        exception_type=SimpleMetadataError,
        value="new_illegal_configuration",
        label="Attribute already defined",
        expected="Once defined, class-level attributes of Simple structures are immutable and cannot be altered.",
        problem="The attribute 'locked_attribute' is already assigned on the class and locked with value: 'active_configuration'.",
        context="Attempted to mutate attribute 'locked_attribute' on the definition class 'DummyBlueprint'.",
        how_to_fix=(
            "Simple system blueprint classes protect their definition definitions via 'Write-Once' constraints.",
            "Modifying already initialized structural attributes or configuration parameters at runtime is strictly disallowed.",
            "Review the runtime execution path to locate why a class-level attribute override was triggered.",
            "If dynamic, stateful instance logic is required, manipulate instance-level attributes rather than class-level blueprints.",
        ),
        verbose=False
    )