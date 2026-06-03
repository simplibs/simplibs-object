from datetime import datetime
from ..base_class import SimpleMixin
from ._history_helpers import build_snapshot, restore_snapshot

class HistoryMixin(SimpleMixin):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je interní formát: name_snake → (path_tuple, value).
    """

    __slots__ = ("_history", "_history_order", "_history_index", "_history_limit")
    
    def __init__(self):
        self._history = {}
        self._history_order = []
        self._history_index = None
        self._history_limit = None

    # ---------------------------------------------------------
    # Inicializace mixinu
    # ---------------------------------------------------------
    def init_mixins(self):
        super().init_mixins()
        # Inicializace úložiště historie
        object.__setattr__(self, "_history", {})
        object.__setattr__(self, "_history_order", [])
        object.__setattr__(self, "_history_index", None)
        object.__setattr__(self, "_history_limit", None)
        # Uložení počátečního stavu
        self.record_state()

    @property
    def history(self):
        return self._history

    @property
    def history_index(self):
        return self._history_index

    @property
    def history_limit(self):
        return self._history_limit

    @history_limit.setter
    def history_limit(self, value: int) -> None:
        if not isinstance(value, int) and value < 1:
            raise ...
        self._history_limit = value


    # ---------------------------------------------------------
    # Vytvoření snapshotu
    # ---------------------------------------------------------
    def record_state(self):
        """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""

        # 1. Vytvoření timestamp a snapshotu
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        snapshot = build_snapshot(self)

        # 2. Kontrola zda je míto v historii
        if self.history_limit and len(self.history) >= self.history_limit:
            first_key = next(iter(self.history))
            self.history.pop(first_key)

        # 3. Zápis do historie a indexu
        self.history[timestamp] = snapshot
        self._history_order.append(timestamp)
        self._history_index = self._history_order.index(snapshot)

        # 4. Navrácení timestamp
        return timestamp

    # ---------------------------------------------------------
    # Získání historie
    # ---------------------------------------------------------
    def get_sorted_history(self):
        """Vrátí seznam (timestamp, snapshot) seřazený podle času."""
        return sorted(self._history.items())

    # ---------------------------------------------------------
    # Undo & Redo  & Gotu & Restore
    # ---------------------------------------------------------

    def undo(self):
        """Vrátí stav instance o jeden snapshot zpět."""

        # 1. Kontrola zda je kam jít
        if self._history_index <= 0:
            return False

        # 2. Změna indexu
        self._history_index -= 1

        # 3. Získání klíče
        timestamp = self._history_order[self._history_index]

        # 4. Získání snapshotu
        snapshot = self.history.get(timestamp)

        # 5. Změna stavu
        restore_snapshot(self, snapshot)
        return True

    def redo(self):
        """Vrátí stav instance o jeden snapshot dopředu."""

        # 1. Kontrola zda je kam jít
        if self._history_index >= len(self._history_order) - 1:
            return False

        # 2. Změna indexu
        self._history_index += 1

        # 3. Získání klíče
        timestamp = self._history_order[self._history_index]

        # 4. Získání snapshotu
        snapshot = self.history.get(timestamp)

        # 5. Změna stavu
        restore_snapshot(self, snapshot)
        return True

    def go_to_last(self):
        """Obnoví aktuální snapshot podle indexu."""

        # 1. Získání klíče
        timestamp = self._history_order[-1]

        # 2. Získání snapshotu
        snapshot = self._history[timestamp]

        # 3. Změna stavu
        restore_snapshot(self, snapshot)

        # 4. Změna indexu
        self._history_index = len(self._history_order) - 1

    def go_to_timestamp(self, timestamp):

        # 1. Kontrola zda je v historii obsažen
        if timestamp not in self._history:
            raise KeyError(f"No snapshot found for timestamp {timestamp}")

        # Získání snapshotu
        snapshot = self._history[timestamp]

        # 3. Změna stavu
        restore_snapshot(self, snapshot)

        # 4. Změna indexu
        self._history_index = self._history_order.index(timestamp)

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
        _history = [(ts, self._history[ts]) for ts in self._history_order]
        for ts, snapshot in _history:
            # Obnovíme snapshot do dočasné kopie
            temp = self.clone()
            restore_snapshot(temp, snapshot)
            export[ts] = temp.to_dict()
        return export
