from datetime import datetime


def resolve_snapshot(key: int | datetime | tuple, history: list) -> tuple:
    """
    Převede klíč na snapshot.
    Přijímá: index (int), timestamp (datetime), nebo přímo snapshot (tuple).
    """

    # 1. Přímý snapshot → vrátíme rovnou
    if isinstance(key, tuple):
        return key

    # 2. Index
    if isinstance(key, int):
        if not (0 <= key < len(history)):
            raise IndexError(f"Snapshot index {key} out of range (history length: {len(history)})")
        _, snapshot = history[key]
        return snapshot

    # 3. Timestamp
    if isinstance(key, datetime):
        for ts, snapshot in history:
            if ts == key:
                return snapshot
        raise KeyError(f"No snapshot found for timestamp {key!r}")

    # 4. Neznámý typ
    raise TypeError(f"Expected int, datetime or tuple, got {type(key).__name__!r}")