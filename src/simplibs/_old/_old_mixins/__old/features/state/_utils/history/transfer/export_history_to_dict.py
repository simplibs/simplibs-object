# Outers
from ......_constants import OWNER_CLASS, HISTORY


def export_history_to_dict(self) -> dict:
    """
    Exportuje historii do přenositelného formátu:
        { _owner_class: ..., history: [ (timestamp, [values...]) ] }
    """
    return {
        OWNER_CLASS: self.meta.owner_class,
        HISTORY: {
            timestamp: snapshot
            for timestamp, snapshot in self._history
        }
    }