from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.validate_mixin_is_simple_base_subclass import (
    validate_mixin_is_simple_base_subclass,
)


def test_validate_mixin_is_simple_base_subclass_pass(mixin_test_classes) -> None:
    """Tests that a subclass of SimpleMixin passes validation."""

    MyTestMixin, MyTestObject = mixin_test_classes
    validate_mixin_is_simple_base_subclass(MyTestObject, MyTestMixin)


def test_validate_mixin_is_simple_base_subclass_raises_error(subtests, mixin_test_classes) -> None:
    """Tests that a class not inheriting from SimpleMixin raises SimpleInitializationError."""

    _, MyTestObject = mixin_test_classes

    class InvalidMixin:
        pass

    assert_exception_function(
        subtests,
        validate_mixin_is_simple_base_subclass,
        invalid_params=(MyTestObject, InvalidMixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID MIXIN",
        label="mixin_not_subclass_of_simplemixin",
        value=InvalidMixin,
        expected="Subclass of SimpleMixin",
        problem="Class 'InvalidMixin' does not inherit from SimpleMixin and cannot be used as a mixin for 'MyTestObject'.",
        context="create_instance(cls=MyTestObject, mixin=InvalidMixin)",
        how_to_fix=(
            "Ensure the mixin inherits from SimpleMixin.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            "        __slots__ = ()\n",
            "If the class is not intended to be a mixin, do not pass it to create_instance.",
        ),
        exception=TypeError,
        verbose=False,
    )