from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.alias_typings import NodesTuple, SnapshotDict


def create_snapshot_dict(
    nodes_tuple: "NodesTuple"
) -> "SnapshotDict":
    """Vytvoří zápis aktuálního snapshotu jako dict s name_snake jako klíči"""
    # noinspection PyProtectedMember
    return {
        instance.meta.name_snake: instance._value
        for instance, _ in nodes_tuple
    }