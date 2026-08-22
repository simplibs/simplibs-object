from types import SimpleNamespace
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_any.utils.validations.raise_with_any_unknown_name import (
    raise_with_any_unknown_name,
)


def test_raise_with_any_unknown_name(subtests) -> None:
    """Tests that raise_with_any_unknown_name raises SimpleRuntimeError with KeyError."""

    class MyClass:
        _constant_names_set = {"const_a"}
        meta = SimpleNamespace(node_names_set={"comp_b"})

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        raise_with_any_unknown_name,
        invalid_params=(dummy_instance, "unknown_key", 42),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY UNKNOWN UPDATE NAME",
        label="update name",
        value="'unknown_key'",
        expected="A valid constant or composite name defined in the instance metadata.",
        problem=(
            "The provided update name does not match any known constant or composite node.",
            "Name 'unknown_key' is not part of the instance structure.",
        ),
        context=(
            "Immutable update attempted on instance 'MyClass'.",
            "Provided value: 42",
            "Allowed constants: {'const_a'}",
            "Allowed composites: ('comp_b',)",
        ),
        how_to_fix=(
            "Ensure the update name corresponds to an existing constant or composite node.",
            "Check the instance metadata for valid names.",
            "Verify that the name is spelled correctly.",
            "Use `instance.meta.node_names_set` or `instance._constant_names_set` to inspect valid keys.",
        ),
        exception=KeyError,
        verbose=False,
    )