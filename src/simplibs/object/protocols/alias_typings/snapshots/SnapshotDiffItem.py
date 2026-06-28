from typing import TypeAlias, Any


# Jeden záznam o změně: trojice (cesta_k_prvku, stará_hodnota, nová_hodnota)
SnapshotDiffItem: TypeAlias = tuple[str, Any, Any]