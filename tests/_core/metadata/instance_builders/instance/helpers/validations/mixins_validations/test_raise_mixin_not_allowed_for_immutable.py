from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.raise_mixin_not_allowed_for_immutable import (
    raise_mixin_not_allowed_for_immutable,
)


def test_raise_mixin_not_allowed_for_immutable(subtests, mixin_test_classes) -> None:
    """Tests that raise_mixin_not_allowed_for_immutable raises SimpleInitializationError."""

    MyTestMixin, MyTestObject = mixin_test_classes

    assert_exception_function(
        subtests,
        raise_mixin_not_allowed_for_immutable,
        invalid_params=(MyTestObject, MyTestMixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID MIXIN USAGE",
        label="mixin_mutable_only_not_allowed_for_immutable",
        value=MyTestMixin,
        expected="Mixin usable only for mutable instances",
        problem=(
            "Mixin 'MyTestMixin' is marked as _mutable_only=True and "
            "cannot be applied to immutable class 'MyTestObject'."
        ),
        context="create_instance(cls=MyTestObject, mixin=MyTestMixin)",
        how_to_fix=(
            "Use this mixin only when creating mutable instances (mutable=True).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), mutable=True)\n",
            "If the mixin should support immutable instances, remove the flag:",
            "    _mutable_only = False",
        ),
        exception=TypeError,
        verbose=False,
    )