from datetime import datetime
from typing import Self
# Outers
from ..base_class import SimpleMixin
# Inners
from ._history_helpers import (
    build_snapshot,
    restore_snapshot,
    compare_snapshots,
    resolve_snapshot,
    snapshot_to_dict,
    dict_to_snapshot
)


# noinspection PyAttributeOutsideInit
class HistoryMixin(SimpleMixin):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je interní formát: name_snake → (path_tuple, value).
    """

    __slots__ = ("_history", "_history_index", "_history_limit")

    # ---------------------------------------------------------
    # Inicializace mixinu
    # ---------------------------------------------------------
    def init_mixins(self):
        super().init_mixins()
        # Inicializace úložiště historie
        object.__setattr__(self, "_history", [])
        object.__setattr__(self, "_history_index", None)
        object.__setattr__(self, "_history_limit", None)
        # Uložení počátečního stavu
        self.record_state()

    @property
    def history(self):
        return tuple(self._history)

    @property
    def history_dict(self):
        return {ts: snapshot for ts, snapshot in self._history}

    @property
    def history_index(self):
        return self._history_index

    @property
    def history_limit(self):
        return self._history_limit

    @history_limit.setter
    def history_limit(self: Self, value: int) -> None:
        if not isinstance(value, int) or value < 1:  # ❌ bylo 'and', má být 'or'
            raise ValueError(f"history_limit must be a positive integer, got {value!r}")

        # Ořezání pokud je aktuální historie delší než nový limit
        if len(self._history) > value:
            del self._history[:len(self._history) - value]
            self._history_index = len(self._history) - 1

        self._history_limit = value


    # ---------------------------------------------------------
    # Vytvoření snapshotu
    # ---------------------------------------------------------
    def record_state(self):
        """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""

        # 1. Vytvoření timestamp a snapshotu
        timestamp = datetime.now()
        snapshot = build_snapshot(self)

        # 2. Kontrola zda je historie v rámci limitu (pokud je nastaven)
        if self._history_limit and len(self._history) >= self._history_limit:
            self._history.pop(0)

        # 3. Zápis do historie a indexu
        self._history.append((timestamp, snapshot))
        self._history_index = len(self._history)-1

        # 4. Navrácení timestamp
        return timestamp


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

        # 3. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)
        return True

    def redo(self):
        """Vrátí stav instance o jeden snapshot dopředu."""

        # 1. Kontrola zda je kam jít
        if self._history_index >= len(self._history) - 1:
            return False

        # 2. Změna indexu
        self._history_index += 1

        # 3. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)
        return True

    def go_to_last(self):
        """Obnoví poslední snapshot v historii."""
        if not self._history:
            return False

        # 1. Změna indexu
        self._history_index = len(self._history) - 1

        # 2. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)
        return True

    def go_to_index(self, index: int):
        """Obnoví snapshot na daném indexu."""

        # 1. Kontrola zda index existuje
        if not (0 <= index < len(self._history)):
            raise IndexError(f"Snapshot index {index} is out of range (history length: {len(self._history)})")

        # 2. Změna indexu
        self._history_index = index

        # 3. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)

    def go_to_timestamp(self, timestamp: datetime):
        """Obnoví snapshot pro daný timestamp."""

        # 1. Vyhledání indexu
        for i, (ts, snapshot) in enumerate(self._history):
            if ts == timestamp:
                # 2. Změna indexu a obnovení stavu
                self._history_index = i
                restore_snapshot(self, snapshot)
                return

        # 3. Timestamp nenalezen
        raise KeyError(f"No snapshot found for timestamp {timestamp!r}")

    # ---------------------------------------------------------
    # Diff mezi snapshoty
    # ---------------------------------------------------------
    # Na instanci — history se doplní automaticky
    def diff(self, a, b, leaves_only=False):
        snap1 = resolve_snapshot(a, self._history)
        snap2 = resolve_snapshot(b, self._history)
        return compare_snapshots(snap1, snap2, leaves_only=leaves_only)

    # Statická — pro přímé snapshoty, history není potřeba
    @staticmethod
    def diff_snapshots(a: tuple, b: tuple, leaves_only: bool = False):
        return compare_snapshots(a, b, leaves_only=leaves_only)


    # ---------------------------------------------------------
    # Export historie (bez interních adres)
    # ---------------------------------------------------------

    def export_history(self):
        return list(self._history)

    def import_history(self, new_history):

        # 1. Vytvoření zálohy existující
        backup_history = self._history

        # 2. Pokus o přepsání historie
        try:
            self._history = list(new_history)
            self.go_to_last()
            self.history_limit = self._history_limit

        # 3. Pokud selže - obnova dat a vyvolání výjimky
        except Exception as e:
            self._history = backup_history
            self.go_to_last()
            raise ...

    def export_history_to_dict(self):
        """
        Exportuje historii do čitelného formátu:
            timestamp → to_dict() stav
        """
        return {ts: snapshot_to_dict(snapshot) for ts, snapshot in self._history}

    def import_history_from_dict(self, history_dict):
        """
        Exportuje historii do čitelného formátu:
            timestamp → to_dict() stav
        """

        # 1. Získání listu ze slovníku
        history_list = [
            (ts, dict_to_snapshot(snapshot_dict))
            for ts, snapshot_dict in history_dict.items()
        ]

        # 2. Přepis historie
        self.import_history(history_list)
