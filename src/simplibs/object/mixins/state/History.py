from datetime import datetime
# Outers
from ..core_mixins import Snapshot, Serialization
# Inners
from ._utils.history.base import set_history_limit, record_state, find_snapshot
from ._utils.history.transfer import export_history_to_dict, import_history_from_dict
from ._utils.history.navigations import (
    history_undo,
    history_redo,
    go_to_last_history,
    go_to_history_on_timestamp,
    go_to_history_on_index
)


# noinspection PyAttributeOutsideInit
# noinspection PyProtectedMember
class History(Snapshot, Serialization):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je čisté tuple hodnot ve stejném pořadí jako _nodes_tuple.
    """

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ("_history", "_history_index", "_history_limit", "_history_count")

    # ---------------------------------------------------------
    # Inicializace mixinu
    # ---------------------------------------------------------
    # Inicializace mixinu
    def init_mixins(self):
        super().init_mixins()
        self._history = []
        self._history_index = None
        self._history_limit = None
        self._history_count = 0
        self.record_state()

    # ---------------------------------------------------------
    # Vytvoření snapshotu historie
    # ---------------------------------------------------------

    def record_state(self) -> datetime:
        """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""
        return record_state(self)

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def history(self):
        """Vrátí historii jako tuple"""
        return tuple(self._history)

    @property
    def history_index(self):
        """Vrátí index poslední historie"""
        return self._history_index

    @property
    def history_limit(self):
        """Vrátí hodnotu limitu velikosti historie"""
        return self._history_limit

    @history_limit.setter
    def history_limit(self, value: int) -> None:
        """Nastaví hodnotu limitu velikosti historie"""
        set_history_limit(self, value)

    def remove_history_limit(self):
        """Odebere limit velikosti historie"""
        self._history_limit = None

    # ---------------------------------------------------------
    # Undo & Redo & GoTo
    # ---------------------------------------------------------

    def undo(self) -> bool:
        """Metodea pro přechod na předchozí záznam (pokud existuje)."""
        return history_undo(self)

    def redo(self) -> bool:
        """Metodea pro přechod na následující záznam (pokud existuje)."""
        return history_redo(self)

    def go_to_last(self):
        """Metodea pro přechod na poslední záznam historie."""
        return go_to_last_history(self)

    def go_to_index(self, index: int):
        """Metoda pro přechod na konkrétní index"""
        return go_to_history_on_index(self, index)

    def go_to_timestamp(self, timestamp: datetime):
        """Metoda pro přechod na konkrétní timestamp"""
        return go_to_history_on_timestamp(self, timestamp)

    # ---------------------------------------------------------
    # Export & Import
    # ---------------------------------------------------------

    def export_history_to_dict(self) -> dict:
        """Exportuje historii do slovníku"""
        return export_history_to_dict(self)

    def import_history_from_dict(self, history_dict: dict):
        """Importuje historii ze slovníku"""
        import_history_from_dict(self, history_dict)

    # ---------------------------------------------------------
    # Diff
    # ---------------------------------------------------------

    def diff(self,
        snap1: int | datetime,
        snap2: int | datetime,
        *,
        constants_only: bool = False
    ) -> tuple:
        """Porovná dva snapshoty — vrátí tuple změněných (path, old_value, new_value)."""
        return self._compare_snapshots(
            find_snapshot(self, snap1),
            find_snapshot(self, snap2),
            constants_only=constants_only
        )
