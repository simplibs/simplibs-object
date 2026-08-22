from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_table_row_not_sequence import (
    raise_bulk_table_row_not_sequence,
)


def test_raise_bulk_table_row_not_sequence(subtests) -> None:
    """Tests that raise_bulk_table_row_not_sequence raises SimpleRuntimeError when a table row is not a sequence."""
    invalid_row = 100
    row_index = 3

    assert_exception_function(
        subtests,
        raise_bulk_table_row_not_sequence,
        invalid_params=(invalid_row, row_index),
        exception_type=SimpleRuntimeError,
        error_name="INVALID BULK TABLE ROW ERROR",
        label="bulk_table_row_is_not_sequence",
        value="int",
        expected="A list or tuple representing a 2D table row",
        problem=(
            "Row at index 3 in the 2D bulk table input is not a sequence "
            "(received type 'int')."
        ),
        context="Attempted bulk creation using 'create_simple_object_bulk_from_table'.",
        how_to_fix=(
            "Ensure every row inside the 2D matrix is wrapped in a list or tuple.",
            "Example format: [[class_name, default, ...], [class_name_2, default_2, ...]]",
        ),
        exception=TypeError,
        verbose=False,
    )