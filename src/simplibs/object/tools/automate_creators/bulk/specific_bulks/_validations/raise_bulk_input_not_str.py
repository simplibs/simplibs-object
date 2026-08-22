from typing import Any, NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_input_not_str(
    value: Any,
    format_name: str,
) -> None | NoReturn:
    """Raises SimpleRuntimeError when bulk text input (CSV/JSON/YAML) is not a string."""

    format_upper = format_name.upper()

    raise SimpleRuntimeError(
        error_name=f"INVALID BULK {format_upper} INPUT ERROR",
        label="bulk_input_is_not_str",
        expected=f"A raw {format_upper} content string",
        value=type(value).__name__,
        problem=(
            f"Bulk creation input for {format_upper} must be a string, "
            f"received type '{type(value).__name__}' instead."
        ),
        context=f"Attempted to parse bulk definitions using 'create_simple_object_bulk_from_{format_name.lower()}'.",
        how_to_fix=(
            f"Ensure the input provided to 'create_simple_object_bulk_from_{format_name.lower()}' is a valid string.",
            f"If reading from a file, make sure to read its text content first (e.g., path.read_text()).",
        ),
        exception=TypeError,
    )