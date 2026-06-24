from ._collect_nodes_data import _collect_nodes_data
# Outers
from ......protocols import SimpleInstanceType


def build_nodes_tuple(self) -> tuple[tuple[SimpleInstanceType, tuple[str, ...]]]:
    """
    Vytvoří tuple s vnitřními tuple (instance, path), kde path obsahuje name_snake názvy vedoucí k danému uzlu.
    """

    # 1. Deinice seznamu
    nodes_list = []

    # 2. Rekuurzivní zběr dat
    _collect_nodes_data(
        instance=self,
        path=(),
        nodes_list=nodes_list
    )

    # Převod a navrácení tuple s hodnotami
    return tuple(nodes_list)