from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.core.validations.raise_unvalide_snopshot_reference import (
    raise_unvalide_snopshot_reference,
)


def test_raise_unvalide_snopshot_reference(subtests) -> None:
    """Tests that raise_unvalide_snopshot_reference raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyHistoryClass"
    invalid_ref = "invalid_string_ref"

    assert_exception_function(
        subtests,
        raise_unvalide_snopshot_reference,
        invalid_params=(dummy_instance, invalid_ref),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY SNAPSHOT REFERENCE ERROR",
        label="snapshot reference",
        expected="Either an integer index or a datetime timestamp.",
        value="str",
        problem=(
            "Invalid snapshot reference provided.",
            "Snapshot lookup requires either an integer index or a datetime timestamp.",
        ),
        context=(
            "History lookup attempted on instance 'MyHistoryClass'.",
            "Provided value type: str",
        ),
        how_to_fix=(
            "Use an integer index to reference snapshots by position.",
            "Use a datetime value to reference snapshots by timestamp.",
            "Do not pass strings, floats, None, or other unsupported types.",
        ),
        exception=TypeError,
        verbose=False,
    )