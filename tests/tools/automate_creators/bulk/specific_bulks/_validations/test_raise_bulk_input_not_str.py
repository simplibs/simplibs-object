import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_input_not_str import (
    raise_bulk_input_not_str,
)


@pytest.mark.parametrize(
    "invalid_value, format_name",
    [
        (12345, "csv"),
        (["json", "as", "list"], "json"),
        ({"yaml": "dict"}, "yaml"),
    ],
)
def test_raise_bulk_input_not_str(subtests, invalid_value, format_name) -> None:
    """Tests that raise_bulk_input_not_str raises SimpleRuntimeError when text input is not a string."""
    format_upper = format_name.upper()

    assert_exception_function(
        subtests,
        raise_bulk_input_not_str,
        invalid_params=(invalid_value, format_name),
        exception_type=SimpleRuntimeError,
        error_name=f"INVALID BULK {format_upper} INPUT ERROR",
        label="bulk_input_is_not_str",
        value=type(invalid_value).__name__,
        expected=f"A raw {format_upper} content string",
        problem=(
            f"Bulk creation input for {format_upper} must be a string, "
            f"received type '{type(invalid_value).__name__}' instead."
        ),
        context=f"Attempted to parse bulk definitions using 'create_simple_object_bulk_from_{format_name.lower()}'.",
        how_to_fix=(
            f"Ensure the input provided to 'create_simple_object_bulk_from_{format_name.lower()}' is a valid string.",
            "If reading from a file, make sure to read its text content first (e.g., path.read_text()).",
        ),
        exception=TypeError,
        verbose=False,
    )