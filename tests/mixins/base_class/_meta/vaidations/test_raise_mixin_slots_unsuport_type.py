from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_slots_unsuport_type import (
    raise_mixin_slots_unsuport_type,
)


def test_raise_mixin_slots_unsuport_type(subtests) -> None:
    """Tests that raise_mixin_slots_unsuport_type raises SimpleRuntimeError."""

    invalid_slots = ["slot1", "slot2"]

    class MyInvalidMixin:
        __slots__ = invalid_slots

    assert_exception_function(
        subtests,
        raise_mixin_slots_unsuport_type,
        invalid_params=(MyInvalidMixin,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="__slots__",
        value=invalid_slots,
        expected="__slots__ must be a tuple or a string.",
        problem=(
            "Mixin 'MyInvalidMixin' defines '__slots__' using an invalid type: list.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Use either a tuple or a string when defining __slots__.",
            "Example: __slots__ = ('a', 'b')",
            "Example: __slots__ = 'a'",
        ),
        exception=TypeError,
        verbose=False,
    )