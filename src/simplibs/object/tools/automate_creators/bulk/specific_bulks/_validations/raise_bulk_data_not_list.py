from typing import Any, NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_data_not_list(
    data: Any,
    format_name: str,
) -> None | NoReturn:
    """Raises SimpleRuntimeError when deserialized bulk data (JSON/YAML) is not a list."""

    format_upper = format_name.upper()

    raise SimpleRuntimeError(
        error_name=f"INVALID BULK {format_upper} DATA STRUCTURE ERROR",
        label="bulk_data_is_not_list",
        expected=f"A list/array of dictionary objects in {format_upper} root",
        value=type(data).__name__,
        problem=(
            f"Parsed {format_upper} payload root must be a list of definition objects, "
            f"received type '{type(data).__name__}' instead."
        ),
        context=f"Attempted bulk creation from parsed {format_upper} data.",
        how_to_fix=(
            f"Ensure the top-level structure in your {format_upper} is a list/array (e.g. '[{{...}}, {{...}}]').",
            "Single objects or key-value maps at root level are not supported for bulk generation.",
        ),
        exception=ValueError,
    )