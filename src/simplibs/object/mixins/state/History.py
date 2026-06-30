from typing import TYPE_CHECKING, Any
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
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.state import HistoryProtocol
    from ...protocols.alias_typings import HistoryEntry, HistoryDict, SnapshotDiffTuple


class History(Snapshot, Serialization):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je čisté tuple hodnot ve stejném pořadí jako _nodes_tuple.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = (
        "_history",
        "_history_index",
        "_history_limit",
        "_history_count"
    )

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "HistoryProtocol"
    ) -> None:
        """
        Metoda, předávající svojí logiku do inicializačního procesu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Vytvoření vnitřních prvků
        self._history: list["HistoryEntry"] = []
        self._history_limit: int | None  = None
        self._history_index: int = 0
        self._history_count: int = 0

        # 3. Vytvření prvního záznamu
        self.record_state()

    # ----------------------------------------
    # Inicializační metoda
    # ----------------------------------------

    def record_state(
        self: "HistoryProtocol"
    ) -> "HistoryEntry":
        """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""
        return record_state(self)

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def history(
        self: "HistoryProtocol"
    ) -> tuple["HistoryEntry", ...]:
        """Vrátí historii jako tuple"""
        return tuple(self._history)

    @property
    def history_index(
        self: "HistoryProtocol"
    ) -> int | None:
        """Vrátí index poslední historie"""
        return self._history_index

    @property
    def history_limit(
        self: "HistoryProtocol"
    ) -> int | None:
        """Vrátí hodnotu limitu velikosti historie"""
        return self._history_limit

    # ----------------------------------------
    # Property - setters
    # ----------------------------------------

    @history_limit.setter
    def history_limit(
        self: "HistoryProtocol",
        value: int
    ) -> None:
        """Nastaví hodnotu limitu velikosti historie"""
        set_history_limit(self, value)

    # ----------------------------------------
    # Methods - UNDO / REDO
    # ----------------------------------------

    def undo(
        self: "HistoryProtocol"
    ) -> bool:
        """Metodea pro přechod na předchozí záznam (pokud existuje)."""
        return history_undo(self)

    def redo(
        self: "HistoryProtocol"
    ) -> bool:
        """Metodea pro přechod na následující záznam (pokud existuje)."""
        return history_redo(self)

    # ----------------------------------------
    # Methods - GOTO
    # ----------------------------------------

    def go_to_last(
        self: "HistoryProtocol"
    ) -> None:
        """Metodea pro přechod na poslední záznam historie."""
        go_to_last_history(self)

    def go_to_index(
        self: "HistoryProtocol",
        index: int
    ) -> None:
        """Metoda pro přechod na konkrétní index"""
        go_to_history_on_index(self, index)

    def go_to_timestamp(
        self: "HistoryProtocol",
        timestamp: datetime
    ) -> None:
        """Metoda pro přechod na konkrétní timestamp"""
        go_to_history_on_timestamp(self, timestamp)

    # ----------------------------------------
    # Methods - EXPORT / IMPORT
    # ----------------------------------------

    def export_history_to_dict(
        self: "HistoryProtocol"
    ) -> "HistoryDict":
        """Exportuje historii do slovníku"""
        return export_history_to_dict(self)

    def import_history_from_dict(
        self: "HistoryProtocol",
        history_dict: "HistoryDict"
    ) -> None:
        """Importuje historii ze slovníku"""
        import_history_from_dict(self, history_dict)

    # ----------------------------------------
    # Methods - REMOVE / DIFF
    # ----------------------------------------

    def remove_history_limit(
        self: "HistoryProtocol"
    ) -> None:
        """Odebere limit velikosti historie"""
        # noinspection PyAttributeOutsideInit
        self._history_limit = None

    def diff(
        self: "HistoryProtocol",
        snap1: int | datetime,
        snap2: int | datetime,
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """Porovná dva snapshoty — vrátí tuple změněných (path, old_value, new_value)."""
        return self._compare_snapshots(
            find_snapshot(self, snap1),
            find_snapshot(self, snap2),
            constants_only=constants_only
        )
