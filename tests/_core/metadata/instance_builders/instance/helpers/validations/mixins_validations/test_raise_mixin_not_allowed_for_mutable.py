from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.raise_mixin_not_allowed_for_mutable import (
    raise_mixin_not_allowed_for_mutable,
)


def test_raise_mixin_not_allowed_for_mutable(subtests, mixin_test_classes) -> None:
    """Tests that raise_mixin_not_allowed_for_mutable raises SimpleInitializationError."""

    MyTestMixin, MyTestObject = mixin_test_classes

    assert_exception_function(
        subtests,
        raise_mixin_not_allowed_for_mutable,
        invalid_params=(MyTestObject, MyTestMixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID MIXIN USAGE",
        label="mixin_immutable_only_not_allowed_for_mutable",
        value=MyTestMixin,
        expected="Mixin usable only for immutable instances",
        problem=(
            "Mixin 'MyTestMixin' is marked as _immutable_only=True and "
            "cannot be applied to mutable class 'MyTestObject'."
        ),
        context="create_instance(cls=MyTestObject, mixin=MyTestMixin)",
        how_to_fix=(
            "Use this mixin only when creating immutable instances (mutable=False).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), mutable=False)\n",
            "If the mixin should support mutable instances, remove the flag:",
            "    _immutable_only = False",
        ),
        exception=TypeError,
        verbose=False,
    )