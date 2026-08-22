from typing import NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_decode_failed(
    raw_content: str,
    format_name: str,
    original_exception: Exception,
) -> None | NoReturn:
    """Raises SimpleRuntimeError when JSON or YAML deserialization fails."""

    format_upper = format_name.upper()

    raise SimpleRuntimeError(
        error_name=f"BULK {format_upper} DECODE ERROR",
        label="bulk_decode_failed",
        expected=f"A valid, syntax-correct {format_upper} formatted string",
        value=raw_content,
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
    )