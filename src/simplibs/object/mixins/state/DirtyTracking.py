from typing import TYPE_CHECKING
# Outers
from ..core_mixins import Snapshot
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.state import DirtyTrackingProtocol
    from ...protocols.alias_typings import SnapshotDiffTuple, SnapshotTuple


class DirtyTracking(Snapshot):
    """
    Moderní dirty tracking založený na snapshotu.
    Funguje pro atomy, composites i nested struktury.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ("_clean_snapshot",)

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "DirtyTrackingProtocol"
    ) -> None:
        """
        Metoda, předávající svojí logiku do inicializačního procesu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Vytvoření snapshotu defaultního stavu
        self._clean_snapshot = self._build_snapshot()

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def is_dirty(
        self: "DirtyTrackingProtocol"
    ) -> bool:
        """True pokud se aktuální stav liší od čistého snapshotu."""
        current_snapshot = self._build_snapshot()
        return current_snapshot != self._clean_snapshot

    @property
    def dirty_paths(
        self: "DirtyTrackingProtocol"
    ) -> "SnapshotDiffTuple":
        """Vrací tuple změněných cest (path, old_value, new_value)."""
        current_snapshot = self._build_snapshot()
        return self._compare_snapshots(
            self._clean_snapshot,
            current_snapshot,
            constants_only=True
        )

    @property
    def clean_snapshot(
        self: "DirtyTrackingProtocol"
    ) -> "SnapshotTuple":
        return self._clean_snapshot

    # ----------------------------------------
    # Methods - GET DIRTY / RESET / MARK CLEAN
    # ----------------------------------------

    def get_dirty_paths(
        self: "DirtyTrackingProtocol",
        *,
        constants_only: bool = True
    ) -> "SnapshotDiffTuple":
        """Vrací změněné cesty s volbou zda jen konstanty nebo vše."""
        return self._compare_snapshots(
            self._clean_snapshot,
            self._build_snapshot(),
            constants_only=constants_only
    )

    def reset_to_clean(
        self: "DirtyTrackingProtocol"
    ) -> None:
        """Vrátí objekt do čistého snapshotu."""
        self._restore_snapshot(self._clean_snapshot)

    def mark_clean(
        self: "DirtyTrackingProtocol"
    ) -> None:
        """Označí aktuální stav jako nový čistý snapshot."""
        # noinspection PyAttributeOutsideInit
        self._clean_snapshot = self._build_snapshot()
