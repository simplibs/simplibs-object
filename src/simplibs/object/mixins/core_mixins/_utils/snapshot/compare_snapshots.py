from typing import TYPE_CHECKING
# Outers
from ...._common.constants import VALUE
# Annotations
if TYPE_CHECKING:
    from .....protocols.alias_typings import SnapshotTuple, NodesTuple, SnapshotDiffTuple


def compare_snapshots(
    nodes_tuple: "NodesTuple",
    snapshot1: "SnapshotTuple",
    snapshot2: "SnapshotTuple",
    *,
    constants_only: bool = False
) -> "SnapshotDiffTuple":

    # 1. Vtyvoření proměných
    diffs = []

    # 2. Procházení snapshotů
    try:

        # 2.1 Cyklus skrtze oba snapshoty
        for (_, path), snap1_value, snap2_value in zip(nodes_tuple, snapshot1, snapshot2):

            # 2.1.1 Přidání hodnoty (pokud jsou rozdílné)
            if (snap1_value != snap2_value and
                not (constants_only and path[-1] == VALUE)):
                diffs.append((path, snap1_value, snap2_value))

        # 2.2 Navrácení tuple se změnami
        return tuple(diffs)

    # 3. Zachycení nevalidních snapshotů
    except (ValueError, TypeError) as e:
        """
        ValueError zachytí rozbalování tuplů špatné délky (not enough values to unpack), 
        TypeError zachytí případ kdy snapshot není iterovatelný vůbec.
        
        Je potřeba dotvořit výjimky!
        """
        raise ValueError(
            f"Snapshots are incompatible and cannot be compared: {e}"
        ) from e

