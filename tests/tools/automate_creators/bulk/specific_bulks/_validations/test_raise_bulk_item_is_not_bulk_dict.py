from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_item_is_not_bulk_dict import (
    raise_bulk_item_is_not_bulk_dict,
)


def test_raise_bulk_item_is_not_bulk_dict(subtests) -> None:
    """Tests that raise_bulk_item_is_not_bulk_dict raises SimpleRuntimeError."""

    invalid_item = {"class_name": "MyConstant", "default": 10}  # dict místo BulkCase
    index = 2

    assert_exception_function(
        subtests,
        raise_bulk_item_is_not_bulk_dict,
        invalid_params=(invalid_item, index),
        exception_type=SimpleRuntimeError,
        error_name="INVALID BULK ITEM ERROR",
        label="bulk_item_is_not_bulk_dict",
        value="dict",
        expected="An instance of BulkCase",
        problem=(
            "Element at index 2 in the bulk creation sequence is not a 'BulkCase' instance "
            "(received type 'dict')."
        ),
        context="Attempted to perform bulk object generation using 'create_simple_object_bulk_from_bulk_dict'.",
        how_to_fix=(
            "Ensure all items passed to bulk creation are wrapped in 'BulkCase' specification instances.",
            "Example: create_simple_object_bulk_from_bulk_dict([BulkCase(class_name='MyConst', default=10), ...])",
        ),
        exception=TypeError,
        verbose=False,
    )