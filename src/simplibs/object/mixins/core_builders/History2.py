from datetime import datetime
from ..base_class import SimpleMixin
from ._history_helpers import build_snapshot, restore_snapshot



class HistoryMixin(SimpleMixin):
    """
    Ukládá kompletní snapshoty stavu instance, umožňuje undo/redo,
    diff mezi snapshoty a export historie.

    Snapshot je interní formát:
        name_snake → (path_tuple, value)
    """

    __slots__ = ("_history", "_history_order", "_history_index", "_history_limit")

    # ---------------------------------------------------------
    # Inicializace mixinu
    # ---------------------------------------------------------
    def init_mixins(self):
        super().init_mixins()

        # Úložiště historie: timestamp → snapshot
        object.__setattr__(self, "_history", {})

        # Pořadí snapshotů (list timestampů)
        object.__setattr__(self, "_history_order", [])

        # Index aktuálního snapshotu
        object.__setattr__(self, "_history_index", -1)

        # Limit historie (None = neomezeně)
        object.__setattr__(self, "_history_limit", None)

        # Uložení počátečního stavu
        self.record_snapshot()

    # ---------------------------------------------------------
    # Vytvoření snapshotu
    # ---------------------------------------------------------
    def record_snapshot(self):
        """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""

        # 1) Vytvoření snapshotu
        snapshot = build_snapshot(self)

        # 2) Timestamp jako unikátní klíč
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

        # 3) Pokud jsme po undo, musíme zahodit "budoucnost"
        if self._history_index < len(self._history_order) - 1:
            # Odřízneme vše za aktuálním indexem
            for ts in self._history_order[self._history_index + 1:]:
                del self._history[ts]
            self._history_order = self._history_order[:self._history_index + 1]

        # 4) Uložení snapshotu
        self._history[timestamp] = snapshot
        self._history_order.append(timestamp)
        self._history_index += 1

        # 5) Limit historie
        if self._history_limit is not None:
            while len(self._history_order) > self._history_limit:
                oldest = self._history_order.pop(0)
                del self._history[oldest]
                self._history_index -= 1

        return timestamp

    # ---------------------------------------------------------
    # Získání historie
    # ---------------------------------------------------------
    def get_history(self):
        """Vrátí seznam (timestamp, snapshot) v pořadí."""
        return [(ts, self._history[ts]) for ts in self._history_order]

    # ---------------------------------------------------------
    # Obnova snapshotu
    # ---------------------------------------------------------
    def restore(self, timestamp):
        """Obnoví stav instance podle snapshotu."""
        snapshot = self._history.get(timestamp)
        if snapshot is None:
            raise KeyError(f"No snapshot found for timestamp {timestamp}")

        restore_snapshot(self, snapshot)

        # Nastavíme index na daný snapshot
        self._history_index = self._history_order.index(timestamp)

    # ---------------------------------------------------------
    # Undo
    # ---------------------------------------------------------
    def undo(self):
        """Vrátí stav instance o jeden snapshot zpět."""
        if self._history_index <= 0:
            return False

        self._history_index -= 1
        ts = self._history_order[self._history_index]
        restore_snapshot(self, self._history[ts])
        return True

    # ---------------------------------------------------------
    # Redo
    # ---------------------------------------------------------
    def redo(self):
        """Vrátí stav instance o jeden snapshot dopředu."""
        if self._history_index >= len(self._history_order) - 1:
            return False

        self._history_index += 1
        ts = self._history_order[self._history_index]
        restore_snapshot(self, self._history[ts])
        return True

    # ---------------------------------------------------------
    # Diff mezi snapshoty
    # ---------------------------------------------------------
    def diff(self, ts1, ts2):
        """
        Vrátí rozdíly mezi dvěma snapshoty.
        Výstup:
            {
                "changed": {path: (old, new)},
                "added": {path: value},
                "removed": {path: value}
            }
        """
        snap1 = self._history.get(ts1)
        snap2 = self._history.get(ts2)

        if snap1 is None or snap2 is None:
            raise KeyError("Invalid snapshot timestamps")

        paths1 = {path: val for _, (path, val) in snap1.items()}
        paths2 = {path: val for _, (path, val) in snap2.items()}

        diff = {
            "changed": {},
            "added": {},
            "removed": {}
        }

        # Změněné hodnoty
        for path in paths1.keys() & paths2.keys():
            if paths1[path] != paths2[path]:
                diff["changed"][path] = (paths1[path], paths2[path])

        # Přidané
        for path in paths2.keys() - paths1.keys():
            diff["added"][path] = paths2[path]

        # Odebrané
        for path in paths1.keys() - paths2.keys():
            diff["removed"][path] = paths1[path]

        return diff

    # ---------------------------------------------------------
    # Export historie (bez interních adres)
    # ---------------------------------------------------------
    def export_history(self):
        """
        Exportuje historii do čitelného formátu:
            timestamp → to_dict() stav
        """
        export = {}
        for ts, snapshot in self.get_history():
            # Obnovíme snapshot do dočasné kopie
            temp = self.clone()
            restore_snapshot(temp, snapshot)
            export[ts] = temp.to_dict()
        return export

