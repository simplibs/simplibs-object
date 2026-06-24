from typing import Any


# noinspection PyProtectedMember
def create_snapshot_dict(nodes_tuple) -> dict[str, Any]:
    """Vytvoří zápis aktuálního snapshotu jako dict s name_snake jako klíči"""
    return {
        instance.meta.name_snake: instance._value
        for instance, _ in nodes_tuple
    }