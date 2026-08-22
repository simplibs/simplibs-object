from typing import NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_csv_callable_not_supported(
    param_name: str,
) -> None | NoReturn:
    """Raises SimpleRuntimeError when executable parameters are specified in CSV input."""

    raise SimpleRuntimeError(
        error_name="BULK CSV CALLABLE UNSUPPORTED ERROR",
        label="bulk_csv_callable_not_supported",
        expected=f"Empty field or omit column '{param_name}' in CSV file",
        value=param_name,
        problem=(
            f"CSV bulk creation does not support executable Python callables or functions "
            f"for parameter '{param_name}'."
        ),
        context="Attempted to parse callable logic or validation handlers from a flat CSV text stream.",
        how_to_fix=(
            f"Remove value from '{param_name}' column when creating objects from CSV.",
            "If your dynamic objects require 'logic', 'validate', or 'decompose' callables, "
            "use JSON, YAML, or direct Python dicts / BulkCase objects instead.",
        ),
        exception=ValueError,
    )