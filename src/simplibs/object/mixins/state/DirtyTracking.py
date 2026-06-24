# Outers
from ..core_mixins import Snapshot


# noinspection PyAttributeOutsideInit
# noinspection PyProtectedMember
class DirtyTracking(Snapshot):
    """
    Moderní dirty tracking založený na snapshotu.
    Funguje pro atomy, composites i nested struktury.
    """

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ("_clean_snapshot",)

    # Inicializace mixinu
    def init_mixins(self):
        super().init_mixins()
        # Uložíme počáteční snapshot jako "čistý"
        self._clean_snapshot = self._build_snapshot()

    # ---------------------------------------------------------
    # Property
    # ---------------------------------------------------------

    @property
    def is_dirty(self) -> bool:
        """True pokud se aktuální stav liší od čistého snapshotu."""
        current_snapshot = self._build_snapshot()
        return current_snapshot != self._clean_snapshot

    @property
    def dirty_paths(self):
        """Vrací tuple změněných cest (path, old_value, new_value)."""
        current_snapshot = self._build_snapshot()
        return self._compare_snapshots(
            self._clean_snapshot,
            current_snapshot,
            constants_only=True
        )

    @property
    def clean_snapshot(self):
        return self._clean_snapshot

    # ---------------------------------------------------------
    # Metody
    # ---------------------------------------------------------

    def get_dirty_paths(self, *, constants_only: bool = True) -> tuple:
        """Vrací změněné cesty s volbou zda jen konstanty nebo vše."""
        return self._compare_snapshots(
            self._clean_snapshot,
            self._build_snapshot(),
            constants_only=constants_only
    )

    def reset_to_clean(self):
        """Vrátí objekt do čistého snapshotu."""
        self._restore_snapshot(self._clean_snapshot)

    def mark_clean(self):
        """Označí aktuální stav jako nový čistý snapshot."""
        self._clean_snapshot = self._build_snapshot()
