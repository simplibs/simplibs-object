from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.raise_mixin_not_allowed_for_composite import (
    raise_mixin_not_allowed_for_composite,
)


def test_raise_mixin_not_allowed_for_composite(subtests, mixin_test_classes) -> None:
    """Tests that raise_mixin_not_allowed_for_composite raises SimpleInitializationError."""

    MyTestMixin, MyTestObject = mixin_test_classes

    assert_exception_function(
        subtests,
        raise_mixin_not_allowed_for_composite,
        invalid_params=(MyTestObject, MyTestMixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID MIXIN USAGE",
        label="mixin_constant_only_not_allowed_for_composite",
        value=MyTestMixin,
        expected="Mixin usable only for atomic (constant) instances",
        problem=(
            "Mixin 'MyTestMixin' is marked as _constant_only=True and "
            "cannot be applied to composite class 'MyTestObject'."
        ),
        context="create_instance(cls=MyTestObject, mixin=MyTestMixin)",
        how_to_fix=(
            "Use this mixin only when creating atomic instances (as_atom=True).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), as_atom=True)\n",
            "If the mixin should support composite instances, remove the flag:",
            "    _constant_only = False",
        ),
        exception=TypeError,
        verbose=False,
    )