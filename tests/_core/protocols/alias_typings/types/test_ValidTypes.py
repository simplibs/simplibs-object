from typing import TypeAlias
from types import UnionType


# Represents acceptable type definitions (e.g., int or int | str)
ValidTypes: TypeAlias = type | UnionType
