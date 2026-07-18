from typing import TypeAlias, Any


# Rekonstrukční plán pro pickle: (třída, prázdné_argumenty, slovník_stavu)
PicklePlan: TypeAlias = tuple[type, tuple[()], dict[str, Any]]