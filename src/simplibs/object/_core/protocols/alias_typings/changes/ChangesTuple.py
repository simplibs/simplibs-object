from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .ChangeTuple import ChangeTuple


# Complex input for bulk changes: tuple of change pairs
ChangesTuple: TypeAlias = tuple["ChangeTuple", ...]