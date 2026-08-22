from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_only_types_invalid import (
    raise_mixin_only_types_invalid,
)


def test_raise_mixin_only_types_invalid(subtests) -> None:
    """Tests that raise_mixin_only_types_invalid raises SimpleRuntimeError."""

    invalid_only_types = ["int", "float"]

    class MyInvalidMixin:
        _only_types = invalid_only_types

    assert_exception_function(
        subtests,
        raise_mixin_only_types_invalid,
        invalid_params=(MyInvalidMixin,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="_only_types",
        value=invalid_only_types,
        expected="UNSET, type, tuple[type, ...], or UnionType.",
        problem=(
            "Mixin 'MyInvalidMixin' defines '_only_types' using an unsupported value:",
            "• ['int', 'float'] (type: list)",
            "This value does not match any of the allowed structural forms.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Use one of the supported forms for '_only_types':",
            "UNSET",
            "a single type (e.g., int)",
            "a tuple of types (e.g., (int, float))",
            "a UnionType (e.g., int | float)",
            "If the flag is not needed, remove it from the mixin.",
        ),
        exception=TypeError,
        verbose=False,
    )