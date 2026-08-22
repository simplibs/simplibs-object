from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_slots_contains_forbidden_slot_names import (
    raise_mixin_slots_contains_forbidden_slot_names,
)


def test_raise_mixin_slots_contains_forbidden_slot_names(subtests) -> None:
    """Tests that raise_mixin_slots_contains_forbidden_slot_names raises SimpleRuntimeError."""

    class MyInvalidMixin:
        pass

    slots_set = {"_value", "_owner", "custom_slot"}

    assert_exception_function(
        subtests,
        raise_mixin_slots_contains_forbidden_slot_names,
        invalid_params=(MyInvalidMixin, slots_set),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="Forbidden slot names in __slots__",
        value=("_owner", "_value"),
        expected="Mixin __slots__ must not contain names reserved by the Simple system.",
        problem=(
            "Mixin 'MyInvalidMixin' defines forbidden slot names inside '__slots__':",
            "• _owner",
            "• _value",
            "These names are reserved for internal Simple system mechanics.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Remove all forbidden names from the __slots__ definition.",
            "Use unique, non-conflicting slot identifiers.",
            "Recommended: prefix mixin slots with '_mx_' or '_mixin_'.",
        ),
        exception=TypeError,
        verbose=False,
    )