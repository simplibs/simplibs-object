from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_slots_is_not_defined import (
    raise_mixin_slots_is_not_defined,
)


def test_raise_mixin_slots_is_not_defined(subtests) -> None:
    """Tests that raise_mixin_slots_is_not_defined raises SimpleRuntimeError."""

    class MyInvalidMixin:
        pass

    assert_exception_function(
        subtests,
        raise_mixin_slots_is_not_defined,
        invalid_params=(MyInvalidMixin,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="__slots__",
        value="MyInvalidMixin",
        expected="Mixin must define its own __slots__ (not inherited).",
        problem=(
            "Mixin 'MyInvalidMixin' does not define its own '__slots__'. ",
            "Inherited slots are not allowed for mixins.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Add an explicit __slots__ definition to the mixin.",
            "Example: __slots__ = ('my_attr',)",
            "Ensure that __slots__ are not inherited from a parent class.",
        ),
        exception=TypeError,
        verbose=False,
    )