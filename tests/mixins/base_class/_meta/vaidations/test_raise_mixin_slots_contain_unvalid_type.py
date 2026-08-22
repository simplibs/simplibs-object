from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_slots_contain_unvalid_type import (
    raise_mixin_slots_contain_unvalid_type,
)


def test_raise_mixin_slots_contain_unvalid_type(subtests) -> None:
    """Tests that raise_mixin_slots_contain_unvalid_type raises SimpleRuntimeError."""

    invalid_slots = ("attr1", 123)

    class DummyClass:
        __name__ = "MyInvalidMixin"
        __dict__ = {"__slots__": invalid_slots}

    dummy_cls = DummyClass()

    assert_exception_function(
        subtests,
        raise_mixin_slots_contain_unvalid_type,
        invalid_params=(dummy_cls,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="__slots__",
        value=invalid_slots,
        expected="All items inside __slots__ must be strings.",
        problem=(
            "Mixin 'MyInvalidMixin' defines '__slots__' with invalid items. ",
            "Every slot name must be of type 'str'.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Ensure that all items inside __slots__ are strings.",
            "Example: __slots__ = ('flag', 'counter')",
        ),
        exception=TypeError,
        verbose=False,
    )