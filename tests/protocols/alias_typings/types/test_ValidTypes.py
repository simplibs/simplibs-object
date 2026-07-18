from typing import TypeAlias
from types import UnionType


# Reprezentuje akceptovatelné typové definice (např. int nebo int | str)
ValidTypes: TypeAlias = type | UnionType
