from typing import Any, Iterable, TYPE_CHECKING
# Inners
from .BulkCase import BulkCase
from .._validations import raise_bulk_item_is_not_bulk_dict

# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike, SimpleInstanceLike


def create_simple_object_bulk_from_bulk_dict(
    bulk_dicts: Iterable[BulkCase],
) -> list["SimpleClassLike | SimpleInstanceLike"]:
    """Generates multiple SimpleConstant or SimpleObject blueprints/instances from BulkCase specifications.

    Args:
        bulk_dicts: Iterable collection containing BulkCase specification instances.

    Returns:
        List of generated Simple class blueprints or instantiated objects.

    Raises:
        SimpleDefinitionError: If any element in the iterable is not an instance of BulkCase.
    """

    results: list[Any] = []

    # 1. Iterate and validate each bulk dictionary item
    for index, item in enumerate(bulk_dicts):

        # 2. Validation that item is an instance of the BulkCase class
        if not isinstance(item, BulkCase):
            raise_bulk_item_is_not_bulk_dict(item, index)

        # 2. Execute dynamic creation for valid item
        results.append(item.create_simple_object())

    # 3. Return aggregated creation outputs
    return results


_DESIGN_NOTES = """
# create_simple_object_bulk_from_bulk_dict (Bulk Processing Engine)

## Purpose
Executes batch dynamic generation of `SimpleConstant` and `SimpleObject` blueprints or 
instances from an iterable of pre-validated `BulkCase` specification objects.

## Execution Workflow
1. Iterates through the provided `bulk_dicts` collection with item tracking.
2. Validates each element's type using `validate_bulk_item_is_bulk_dict`.
3. Invokes `create_simple_object()` on each `BulkCase` instance to produce the class/object.
4. Aggregates and returns the results in a python list.

## Framework Usage
- Internal engine backing bulk object definition workflows.
"""