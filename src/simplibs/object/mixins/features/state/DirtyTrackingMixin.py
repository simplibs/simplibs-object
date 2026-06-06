# Outers
from ..base_class import SimpleMixin
# Inners
from ._history_helpers import (
    build_snapshot,
    restore_snapshot,
    compare_snapshots,
)


class DirtyTrackingMixin(SimpleMixin):
    """
    Moderní dirty tracking založený na snapshotu.
    Funguje pro atomy, composites i nested struktury.
    """
    __slots__ = ("_clean_snapshot",)

    def init_mixins(self):
        super().init_mixins()
        # Uložíme počáteční snapshot jako "čistý"
        object.__setattr__(self, "_clean_snapshot", build_snapshot(self))

    # ---------------------------------------------------------
    # Dirty flag
    # ---------------------------------------------------------
    @property
    def is_dirty(self) -> bool:
        """True pokud se aktuální stav liší od čistého snapshotu."""
        current = build_snapshot(self)
        return current != self._clean_snapshot

    # ---------------------------------------------------------
    # Dirty paths (diff)
    # ---------------------------------------------------------
    @property
    def dirty_paths(self):
        """Vrací tuple změněných cest (path, old_value, new_value)."""
        current = build_snapshot(self)
        return compare_snapshots(self._clean_snapshot, current, leaves_only=True)

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------
    def reset(self):
        """Vrátí objekt do čistého snapshotu."""
        restore_snapshot(self, self._clean_snapshot)

    # ---------------------------------------------------------
    # Mark clean
    # ---------------------------------------------------------
    def mark_clean(self):
        """Označí aktuální stav jako nový čistý snapshot."""
        object.__setattr__(self, "_clean_snapshot", build_snapshot(self))
