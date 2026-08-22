from types import SimpleNamespace
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_any.utils.validations.raise_split_changes_unknown_name import (
    raise_split_changes_unknown_name,
)


def test_raise_split_changes_unknown_name(subtests) -> None:
    """Tests that raise_split_changes_unknown_name raises SimpleRuntimeError with KeyError."""

    class MyClass:
        _constant_names_set = {"const_a"}
        meta = SimpleNamespace(node_names_set={"comp_b"})

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        raise_split_changes_unknown_name,
        invalid_params=(dummy_instance, "unknown_key"),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY UNKNOWN UPDATE NAME (split_changes)",
        label="update name",
        value="'unknown_key'",
        expected="A valid constant or composite name defined in the instance metadata.",
        problem=(
            "The provided update name does not match any known constant or composite node.",
            "Name 'unknown_key' is not part of the instance structure.",
        ),
        context=(
            "Classification attempted on instance 'MyClass'.",
            "Allowed constants: {'const_a'}",
            "Allowed composites: ('comp_b',)",
        ),
        how_to_fix=(
            "Ensure the update name corresponds to an existing constant or composite node.",
            "Check the instance metadata for valid names.",
            "Verify that the name is spelled correctly.",
        ),
        exception=KeyError,
        verbose=False,
    )