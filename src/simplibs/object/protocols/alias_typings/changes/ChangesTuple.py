from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .ChangeTuple import ChangeTuple


# Komplexní vstup pro hromadné změny: buď jedna dvojice, n-tice dvojic, nebo nic
# ChangesTuple: TypeAlias = "ChangeTuple" | tuple["ChangeTuple", ...] | None
ChangesTuple: TypeAlias = tuple["ChangeTuple", ...]