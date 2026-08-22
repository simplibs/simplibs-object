import pytest
from typing import Any

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.property_builders.value_helpers.validations.raise_locked_value_error import (
    raise_locked_value_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, value",
    [
        ("UserConfig", 42),
        ("SnapshotObject", "new_string_value"),
        ("CompositeInstance", [1, 2, 3]),
    ],
)
def test_raise_locked_value_error(
    subtests, class_name: str, value: Any
) -> None:
    """Test that attempting to modify a locked instance raises SimpleRuntimeError."""

    assert_exception_function(
        subtests,
        raise_locked_value_error,

        invalid_params=(value, class_name),
        exception_type=SimpleRuntimeError,

        error_name="VALUE LOCKED",
        label="value_is_locked",
        expected="Unlocked instance",
        value=value,
        problem=(
            f"Instance '{class_name}' is locked and its value "
            f"cannot be modified."
        ),
        context=f"{class_name}.value = {value}",
        how_to_fix=(
            "Unlock the instance before modifying its value.",
            "If the instance uses the Permission mixin, call:",
            "    obj.unlock()",
            "If the instance exposes '_locked' directly, set:",
            "    obj._locked = False",
        ),
        exception=AttributeError,

        verbose=False,
    )