from typing import TypeAlias, Any


# Reprezentuje imutabilní otisk (snapshot) hodnot všech vnitřních prvků kompozice
SnapshotTuple: TypeAlias = tuple[Any, ...]