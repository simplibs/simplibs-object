from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_dict_contains_forbidden_attributes import (
    raise_mixin_dict_contains_forbidden_attributes,
)


def test_raise_mixin_dict_contains_forbidden_attributes(subtests) -> None:
    """Tests that raise_mixin_dict_contains_forbidden_attributes raises SimpleRuntimeError."""

    class MyInvalidMixin:
        value = 123
        _owner = None
        custom_attr = "ok"

    assert_exception_function(
        subtests,
        raise_mixin_dict_contains_forbidden_attributes,
        invalid_params=(MyInvalidMixin,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="Forbidden class attributes",
        value=("_owner", "value"),
        expected="Mixin class must not define attributes reserved by the Simple system.",
        problem=(
            "Mixin 'MyInvalidMixin' defines forbidden class-level attributes:",
            "• _owner",
            "• value",
            "These names are reserved for internal Simple system mechanics.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Remove all forbidden attribute names from the mixin class.",
            "Use unique, non-conflicting attribute identifiers.",
            "Recommended: prefix mixin attributes with '_mx_' or '_mixin_'.",
        ),
        exception=TypeError,
        verbose=False,
    )