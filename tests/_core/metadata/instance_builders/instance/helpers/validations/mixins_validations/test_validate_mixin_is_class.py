from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.validate_mixin_is_class import (
    validate_mixin_is_class,
)


def test_validate_mixin_is_class_pass(mixin_test_classes) -> None:
    """Tests that a valid class object passes mixin validation."""

    MyTestMixin, MyTestObject = mixin_test_classes
    validate_mixin_is_class(MyTestObject, MyTestMixin)


def test_validate_mixin_is_class_raises_error(subtests, mixin_test_classes) -> None:
    """Tests that a non-class object raises SimpleInitializationError."""

    _, MyTestObject = mixin_test_classes
    invalid_mixin = "not_a_class"

    assert_exception_function(
        subtests,
        validate_mixin_is_class,
        invalid_params=(MyTestObject, invalid_mixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID MIXIN",
        label="mixin_not_class",
        value=invalid_mixin,
        expected="Class derived from SimpleMixin",
        problem=f"Object '{invalid_mixin!r}' is not a class and cannot be used as a mixin for 'MyTestObject'.",
        context=f"create_instance(cls=MyTestObject, mixin={invalid_mixin!r})",
        how_to_fix=(
            "Pass a class, not an instance or other object.",
            "Correct usage:",
            "    create_instance(MyClass, mixins=(MyMixin,), as_atom=False)",
        ),
        exception=TypeError,
        verbose=False,
    )