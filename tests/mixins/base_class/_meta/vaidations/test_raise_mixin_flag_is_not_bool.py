from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_flag_is_not_bool import (
    raise_mixin_flag_is_not_bool,
)


def test_raise_mixin_flag_is_not_bool(subtests) -> None:
    """Tests that raise_mixin_flag_is_not_bool raises SimpleRuntimeError."""

    class MyInvalidMixin:
        _constant_only = "yes"
        _mutable_only = 1

    assert_exception_function(
        subtests,
        raise_mixin_flag_is_not_bool,
        invalid_params=(MyInvalidMixin,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="Invalid mixin flag types",
        value=(("_constant_only", "yes"), ("_mutable_only", 1)),
        expected="All mixin flags must be boolean (True/False).",
        problem=(
            "Mixin 'MyInvalidMixin' defines one or more flags with invalid types:",
            "• _constant_only = 'yes' (type: str)",
            "• _mutable_only = 1 (type: int)",
            "All declarative mixin flags must be boolean values.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Set each mixin flag to either True or False.",
            "Example: _constant_only = True",
            "Example: _mutable_only = False",
            "If a flag is not needed, remove it from the mixin.",
        ),
        exception=TypeError,
        verbose=False,
    )