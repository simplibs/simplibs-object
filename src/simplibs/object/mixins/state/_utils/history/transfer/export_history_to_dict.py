# Outers
from ......_constants import OWNER_CLASS, HISTORY, MIXINS, IS_MUTABLE, IS_CONSTANT


def export_history_to_dict(self) -> dict:
    """
    Exportuje historii do přenositelného formátu:
        { _owner_class: ..., history: [ (timestamp, [values...]) ] }
    """
    return {
        OWNER_CLASS: self.meta.owner_class,
        MIXINS: self.__class__.__mixins__,
        IS_CONSTANT: self.__class__.__is_constant__,
        IS_MUTABLE: self.__class__.__is_mutable__,
        HISTORY: {
            timestamp: snapshot
            for timestamp, snapshot in self._history
        }
    }