from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.transfer.validations.raise_unvalide_owner_class_mismatch import (
    raise_unvalide_owner_class_mismatch,
)


def test_raise_unvalide_owner_class_mismatch(subtests) -> None:
    """Tests that raise_unvalide_owner_class_mismatch raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyClass"
    dummy_instance.meta.owner_class = "MyClass"

    got_owner_class = "OtherClass"

    assert_exception_function(
        subtests,
        raise_unvalide_owner_class_mismatch,
        invalid_params=(dummy_instance, got_owner_class),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY OWNER CLASS MISMATCH",
        label="owner_class",
        expected="Owner class: MyClass",
        value="'OtherClass'",
        problem=(
            "Imported history belongs to a different class.",
            "History snapshots must originate from the same component type."
        ),
        context=(
            "History import attempted on instance 'MyClass'.",
            "Expected owner class: MyClass",
            "Got owner class: 'OtherClass'"
        ),
        how_to_fix=(
            "Ensure the imported dictionary was produced by the same class.",
            "Use `export_history_to_dict()` on an instance of the correct type.",
            "Do not mix histories between different components."
        ),
        exception=ValueError,
        verbose=False,
    )