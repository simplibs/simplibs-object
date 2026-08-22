import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_decode_failed import (
    raise_bulk_decode_failed,
)


@pytest.mark.parametrize(
    "raw_content, format_name, original_exception",
    [
        ("{invalid json", "json", ValueError("Expecting property name enclosed in double quotes")),
        ("key: [unbalanced", "yaml", Exception("Syntax error in YAML")),
    ],
)
def test_raise_bulk_decode_failed(subtests, raw_content, format_name, original_exception) -> None:
    """Tests that raise_bulk_decode_failed raises SimpleRuntimeError when decoder fails."""
    format_upper = format_name.upper()

    assert_exception_function(
        subtests,
        raise_bulk_decode_failed,
        invalid_params=(raw_content, format_name, original_exception),
        exception_type=SimpleRuntimeError,
        error_name=f"BULK {format_upper} DECODE ERROR",
        label="bulk_decode_failed",
        value=raw_content,
        expected=f"A valid, syntax-correct {format_upper} formatted string",
        problem=(
            f"Failed to parse provided {format_upper} string into structured data. "
            f"Underlying decoder error: {original_exception}"
        ),
        context=f"Attempted to deserialize bulk object definitions from {format_upper} text stream.",
        how_to_fix=(
            f"Verify that the input string is valid {format_upper} syntax.",
            "Check for common syntax errors like missing quotes, trailing commas, or invalid indentation.",
        ),
        exception=ValueError,
        verbose=False,
    )