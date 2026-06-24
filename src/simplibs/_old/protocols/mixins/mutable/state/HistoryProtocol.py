from typing import Protocol, runtime_checkable, Any
from datetime import datetime
# Outers
from ...common.core_logic import SnapshotProtocol
# Inners
from .MutableSerializationProtocol import MutableSerializationProtocol


@runtime_checkable
class HistoryProtocol(SnapshotProtocol, MutableSerializationProtocol, Protocol):
    """
    Protokol pro mixin History.

    Garantuje kompletní správu časové osy objektu (Undo/Redo kaskády),
    včetně navigace na index/timestamp, sledování limitů paměti,
    porovnávání historických snapshotů (diff) a exportu/importu celé historie.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---
    _history: list[dict[str, Any]]  # Vnitřní úložiště časových záznamů
    _history_index: int | None       # Ukazatel na aktuální pozici v historii
    _history_limit: int | None       # Maximální počet povolených záznamů
    _history_count: int              # Celkový počet reálně uložených záznamů

    # --- INICIALIZAČNÍ A ZÁPISOVÁ LOGIKA ---

    def record_state(self) -> datetime:
        """Vytvoří snapshot aktuálního stavu a zapíše jej na časovou osu historie."""
        ...

    # --- PROPERTIES ---

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        """Vrací kompletní časovou osu historie jako neměnné tuple záznamů."""
        ...

    @property
    def history_index(self) -> int | None:
        """Vrací index aktuální pozice (záznamu) v rámci časové osy."""
        ...

    @property
    def history_limit(self) -> int | None:
        """Vrací aktuální limit velikosti historie (kapacitu), nebo None."""
        ...

    @history_limit.setter
    def history_limit(self, value: int) -> None:
        """Nastaví maximální limit velikosti (kapacitu) pro ukládání historie."""
        ...

    def remove_history_limit(self) -> None:
        """Kompletně odebere limit velikosti historie (neomezená časová osa)."""
        ...

    # --- NAVIGAČNÍ API (Undo & Redo & GoTo) ---

    def undo(self) -> bool:
        """
        Posune stav instance o jeden krok zpět v čase (do minulosti).
        Vrací True, pokud byl posun úspěšný, jinak False.
        """
        ...

    def redo(self) -> bool:
        """
        Posune stav instance o jeden krok vpřed v čase (do budoucnosti).
        Vrací True, pokud byl posun úspěšný, jinak False.
        """
        ...

    def go_to_last(self) -> None:
        """Přesune stav instance na nejnovější (poslední) uložený záznam v historii."""
        ...

    def go_to_index(self, index: int) -> None:
        """Přesune stav instance na záznam specifikovaný konkrétním číselným indexem."""
        ...

    def go_to_timestamp(self, timestamp: datetime) -> None:
        """Přesune stav instance na záznam odpovídající konkrétnímu časovému razítku."""
        ...

    # --- EXPORT & IMPORT HISTORIE ---

    def export_history_to_dict(self) -> dict[str, Any]:
        """Exportuje kompletní strukturu a data časové osy do slovníku."""
        ...

    def import_history_from_dict(self, history_dict: dict[str, Any]) -> None:
        """Importuje a kompletně zrekonstruuje celou časovou osu z předaného slovníku."""
        ...

    # --- ANALÝZA ROZDÍLŮ (Diff) ---

    def diff(
        self,
        snap1: int | datetime,
        snap2: int | datetime,
        *,
        constants_only: bool = False
    ) -> tuple[tuple[str, Any, Any], ...]:
        """
        Porovná dva libovolné body v historii (zadané indexem nebo timestampem).
        Vrací n-tici trojic změn: (cesta_k_prvku, stará_hodnota, nová_hodnota).
        """
        ...