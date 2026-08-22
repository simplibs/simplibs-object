from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_csv_callable_not_supported import (
    raise_bulk_csv_callable_not_supported,
)


def test_raise_bulk_csv_callable_not_supported(subtests) -> None:
    """Tests that raise_bulk_csv_callable_not_supported raises SimpleRuntimeError."""
    param_name = "logic"

    assert_exception_function(
        subtests,
        raise_bulk_csv_callable_not_supported,
        invalid_params=(param_name,),
        exception_type=SimpleRuntimeError,
        error_name="BULK CSV CALLABLE UNSUPPORTED ERROR",
        label="bulk_csv_callable_not_supported",
        value=param_name,
        expected="Empty field or omit column 'logic' in CSV file",
        problem=(
            "CSV bulk creation does not support executable Python callables or functions "
            "for parameter 'logic'."
        ),
        context="Attempted to parse callable logic or validation handlers from a flat CSV text stream.",
        how_to_fix=(
            "Remove value from 'logic' column when creating objects from CSV.",
            "If your dynamic objects require 'logic', 'validate', or 'decompose' callables, "
            "use JSON, YAML, or direct Python dicts / BulkCase objects instead.",
        ),
        exception=ValueError,
        verbose=False,
    )