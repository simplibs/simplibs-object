def raise_unvalide_snapshot_index():
    raise IndexError(f"Snapshot index {index} is out of range (history length: {len(self._history)})")
