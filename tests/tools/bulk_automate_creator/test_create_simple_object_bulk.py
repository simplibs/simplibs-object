from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING, Iterable
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .create_simple_object import create_simple_object
from .BulkDict import BulkDict
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassType, SimpleMixinLike



def create_simple_object_bulk_from_bulk_dict(bulk_dicts: Iterable[BulkDict]):

    result = []

    for item in bulk_dicts:
        if not isinstance(item, BulkDict):
            raise TypeError("Každý prvek musí být instance BulkDict.")

        result.append(item.create_simple_object())

    return result