from typing import TYPE_CHECKING
# Outers
from ....._common.constants import (
    OWNER_CLASS,
    HISTORY,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol
    from ......protocols.alias_typings import HistoryDict


def export_history_to_dict(
    self: "HistoryProtocol"
) -> "HistoryDict":
    """
    Exportuje historii do přenositelného formátu:
        { _owner_class: ..., history: ( (timestamp, [values...])... ) }
    """
    return {
        OWNER_CLASS: self.meta.owner_class,
        HISTORY: self.history
    }