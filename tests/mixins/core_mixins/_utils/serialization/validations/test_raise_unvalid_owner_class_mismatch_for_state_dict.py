from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.sentinels import UNSET
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.core_mixins._utils.serialization.validations.raise_unvalid_owner_class_mismatch_for_state_dict import (
    raise_unvalid_owner_class_mismatch_for_state_dict,
)


def test_raise_unvalid_owner_class_mismatch_for_state_dict(subtests) -> None:
    """Tests that raise_unvalid_owner_class_mismatch_for_state_dict raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MySerializableClass"
    dummy_instance.meta.owner_class = "MySerializableClass"

    got_owner_class = "OtherClass"

    assert_exception_function(
        subtests,
        raise_unvalid_owner_class_mismatch_for_state_dict,
        invalid_params=(dummy_instance, got_owner_class),
        exception_type=SimpleRuntimeError,
        error_name="STATE DICT OWNER CLASS MISMATCH",
        label="owner_class",
        value="'OtherClass'",
        expected="Owner class: 'MySerializableClass'",
        problem=(
            "Imported state dictionary belongs to a different class.",
            "State reconstruction requires exact owner class identity.",
        ),
        context=(
            "State import attempted on instance 'MySerializableClass'.",
            "Expected owner class: 'MySerializableClass'",
            "Got owner class: 'OtherClass'",
        ),
        how_to_fix=(
            "Ensure the dictionary was produced by the same class.",
            "Use `to_dict()` or `export_history_to_dict()` on an instance of the correct type.",
            "Do not mix state dictionaries between different component classes.",
            "Verify that OWNER_CLASS is present and correct in the input dictionary.",
        ),
        exception=ValueError,
        verbose=False,
    )


def test_raise_unvalid_owner_class_mismatch_for_state_dict_unset(subtests) -> None:
    """Tests context message when got_owner_class is UNSET."""
    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MySerializableClass"
    dummy_instance.meta.owner_class = "MySerializableClass"

    assert_exception_function(
        subtests,
        raise_unvalid_owner_class_mismatch_for_state_dict,
        invalid_params=(dummy_instance, UNSET),
        exception_type=SimpleRuntimeError,
        error_name="STATE DICT OWNER CLASS MISMATCH",
        label="owner_class",
        value="UNSET",
        expected="Owner class: 'MySerializableClass'",
        problem=(
            "Imported state dictionary belongs to a different class.",
            "State reconstruction requires exact owner class identity.",
        ),
        context=(
            "State import attempted on instance 'MySerializableClass'.",
            "Expected owner class: 'MySerializableClass'",
            "Got owner class: UNSET",
            "Note: If the value is UNSET, the dictionary is missing the required OWNER_CLASS field.",
        ),
        how_to_fix=(
            "Ensure the dictionary was produced by the same class.",
            "Use `to_dict()` or `export_history_to_dict()` on an instance of the correct type.",
            "Do not mix state dictionaries between different component classes.",
            "Verify that OWNER_CLASS is present and correct in the input dictionary.",
        ),
        exception=ValueError,
        verbose=False,
    )