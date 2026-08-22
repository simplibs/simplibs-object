from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.raise_mixin_not_allowed_for_constant import (
    raise_mixin_not_allowed_for_constant,
)


def test_raise_mixin_not_allowed_for_constant(subtests, mixin_test_classes) -> None:
    """Tests that raise_mixin_not_allowed_for_constant raises SimpleInitializationError."""

    MyTestMixin, MyTestObject = mixin_test_classes

    assert_exception_function(
        subtests,
        raise_mixin_not_allowed_for_constant,
        invalid_params=(MyTestObject, MyTestMixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID MIXIN USAGE",
        label="mixin_composite_only_not_allowed_for_constant",
        value=MyTestMixin,
        expected="Mixin usable only for composite instances",
        problem=(
            "Mixin 'MyTestMixin' is marked as _composite_only=True and "
            "cannot be applied to atomic class 'MyTestObject'."
        ),
        context="create_instance(cls=MyTestObject, mixin=MyTestMixin)",
        how_to_fix=(
            "Use this mixin only when creating composite instances (as_atom=False).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), as_atom=False)\n",
            "If the mixin should support atomic instances, remove the flag:",
            "    _composite_only = False",
        ),
        exception=TypeError,
        verbose=False,
    )