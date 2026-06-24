from typing import Protocol, runtime_checkable, Any
# Outers
from ...common.core_logic.SnapshotProtocol import SnapshotProtocol


@runtime_checkable
class DirtyTrackingProtocol(SnapshotProtocol, Protocol):
    """
    Protokol pro mixin DirtyTracking.

    Garantuje schopnost sledovat změny stavu (dirty tracking) v hierarchii objektu
    oproti uloženému "čistému" otisku, vracet změněné cesty a resetovat stav.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Uchovává otisk stavu, který je považován za výchozí "čistý" (nezměněný)
    _clean_snapshot: tuple[Any, ...]

    # --- ERGONOMICKÉ PROPERTIES ---

    @property
    def is_dirty(self) -> bool:
        """Vrací True, pokud se aktuální stav hierarchie liší od čistého otisku."""
        ...

    @property
    def dirty_paths(self) -> tuple[tuple[str, Any, Any], ...]:
        """
        Vrací n-tici změněných cest atomických prvků.
        Každý prvek v n-tici tvoří trojice: (cesta_k_prvku, stará_hodnota, nová_hodnota).
        """
        ...

    @property
    def clean_snapshot(self) -> tuple[Any, ...]:
        """Přístup k aktuálně uloženému čistému snapshotu."""
        ...

    # --- VEŘEJNÉ API PRO SLEDOVÁNÍ ZMĚN ---

    def get_dirty_paths(self, *, constants_only: bool = True) -> tuple[tuple[str, Any, Any], ...]:
        """
        Vrací n-tici detekovaných změn v hierarchii.
        Umožňuje zvolit, zda sledovat pouze konstanty (atomy), nebo i kompozitní uzly.
        """
        ...

    def reset_to_clean(self) -> None:
        """Obnoví kompletní vnitřní stav všech prvků z čistého otisku (zahodí změny)."""
        ...

    def mark_clean(self) -> None:
        """Označí aktuální stav celé instance jako nový výchozí 'čistý' stav."""
        ...