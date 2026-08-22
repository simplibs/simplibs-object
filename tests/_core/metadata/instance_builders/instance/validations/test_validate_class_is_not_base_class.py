from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.validations.validate_class_is_not_base_class import (
    validate_class_is_not_base_class,
)


def test_validate_class_is_not_base_class_pass(sample_object_classes) -> None:
    """Tests that declarative classes pass validation."""

    _, MyTestObject = sample_object_classes
    validate_class_is_not_base_class(MyTestObject)


def test_validate_class_is_not_base_class_raises_error(subtests) -> None:
    """Tests that passing a core base class raises SimpleInitializationError."""

    class SimpleObject:
        __name__ = "SimpleObject"

    assert_exception_function(
        subtests,
        validate_class_is_not_base_class,
        invalid_params=(SimpleObject,),
        exception_type=SimpleInitializationError,
        error_name="INVALID CLASS",
        label="base_class_not_allowed",
        value=SimpleObject,
        expected="Declarative subclass of SimpleBase",
        problem="Class 'SimpleObject' is a core Simple framework base class and cannot be instantiated.",
        context="create_instance(cls=SimpleObject)",
        how_to_fix=(
            "Use a declarative class derived from SimpleObject or SimpleConstant.",
            "Example:",
            "    class MyNumber(SimpleObject):",
            "        _type = int\n",
            "Base classes (SimpleObject, SimpleAtom, SimpleComposite, …) serve only as framework primitives.",
        ),
        exception=TypeError,
        verbose=False,
    )