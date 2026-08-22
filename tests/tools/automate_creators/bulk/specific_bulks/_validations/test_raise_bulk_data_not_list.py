import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_data_not_list import (
    raise_bulk_data_not_list,
)


@pytest.mark.parametrize(
    "invalid_data, format_name",
    [
        ({"class_name": "MyConst"}, "json"),
        ("string_data", "yaml"),
        (123, "JSON"),
    ],
)
def test_raise_bulk_data_not_list(subtests, invalid_data, format_name) -> None:
    """Tests that raise_bulk_data_not_list raises SimpleRuntimeError for non-list payloads."""
    format_upper = format_name.upper()

    assert_exception_function(
        subtests,
        raise_bulk_data_not_list,
        invalid_params=(invalid_data, format_name),
        exception_type=SimpleRuntimeError,
        error_name=f"INVALID BULK {format_upper} DATA STRUCTURE ERROR",
        label="bulk_data_is_not_list",
        value=type(invalid_data).__name__,
        expected=f"A list/array of dictionary objects in {format_upper} root",
        problem=(
            f"Parsed {format_upper} payload root must be a list of definition objects, "
            f"received type '{type(invalid_data).__name__}' instead."
        ),
        context=f"Attempted bulk creation from parsed {format_upper} data.",
        how_to_fix=(
            f"Ensure the top-level structure in your {format_upper} is a list/array (e.g. '[{{...}}, {{...}}]').",
            "Single objects or key-value maps at root level are not supported for bulk generation.",
        ),
        exception=ValueError,
        verbose=False,
    )