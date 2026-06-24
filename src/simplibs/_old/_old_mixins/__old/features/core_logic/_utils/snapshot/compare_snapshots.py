from datetime import datetime
# Outers
from ....._constants import VALUE


def compare_snapshots(
    nodes_tuple: tuple,
    snapshot1: tuple,
    snapshot2: tuple,
    *,
    constants_only: bool = False
) -> tuple:

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

