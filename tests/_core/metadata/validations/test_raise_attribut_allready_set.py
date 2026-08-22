from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.validations.raise_attribut_allready_set import (
    raise_attribut_allready_set,
)


def test_raise_attribut_allready_set(subtests, sample_object_classes) -> None:
    """Tests that raise_attribut_allready_set raises SimpleDefinitionError."""

    _, MyTestObject = sample_object_classes

    attr_name = "_type"
    new_value = float
    current_value = getattr(MyTestObject, attr_name)

    assert_exception_function(
        subtests,
        raise_attribut_allready_set,
        invalid_params=(MyTestObject, attr_name, new_value),
        exception_type=SimpleDefinitionError,
        error_name="CLASS ATTRIBUTE IMMUTABILITY ERROR",
        label="attribute_already_defined",
        value=new_value,
        expected="Write-once class-level attributes",
        problem=(
            f"Attribute '{attr_name}' on class 'MyTestObject' is already initialized "
            f"and locked with value: {current_value!r}."
        ),
        context=f"Attempted to overwrite attribute '{attr_name}' on definition class 'MyTestObject'.",
        how_to_fix=(
            "Class-level blueprint attributes in the Simple system follow a strict 'Write-Once' policy.",
            "Do not modify structural or configuration attributes after they have been initialized.",
            "If dynamic state is required, use instance-level attributes instead of class-level blueprints.",
            "Review the execution path to identify why a second write was attempted.",
        ),
        exception=AttributeError,
        verbose=False,
    )