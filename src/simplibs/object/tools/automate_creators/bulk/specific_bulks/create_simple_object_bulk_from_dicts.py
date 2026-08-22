from typing import Any
# Outers
from ..BulkCase import BulkCase
# Inners
from .create_simple_object_bulk_from_bulk_case_class import create_simple_object_bulk_from_bulk_case_class
from ._validations import raise_bulk_input_not_sequence


def create_simple_object_bulk_from_dicts(dicts: list[dict[str, Any]]):
    """Creates a bulk collection of Simple objects from a sequence of dictionaries."""
    if not isinstance(dicts, (list, tuple)):
        raise_bulk_input_not_sequence(
            value=dicts,
            runner_name="create_simple_object_bulk_from_dicts",
            expected_items_description="dictionaries",
        )

    bulk = tuple(BulkCase(**d) for d in dicts)
    return create_simple_object_bulk_from_bulk_case_class(bulk)