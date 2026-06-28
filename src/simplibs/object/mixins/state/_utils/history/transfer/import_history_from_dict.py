from typing import TYPE_CHECKING, Any
from datetime import datetime
# Outers
from ....._common.constants import (
    OWNER_CLASS,
    HISTORY,
    MIXINS,
    IS_MUTABLE,
    IS_CONSTANT
)
from .._validations import (
    raise_unvalid_snapshot_structure,
    raise_unvalide_history_import_file
)
# Inners
from ._import_history import _import_history
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol


def import_history_from_dict(
    self: "HistoryProtocol",
    history_dict: dict[str, Any]
) -> None:
    """Importuje historii z přenositelného formátu s kontrolou owner_class."""

    # 1. Validace kontejneru
    if (not isinstance(history_dict, dict)
        or len(history_dict) != 2
        or set(history_dict.keys()) == {OWNER_CLASS, HISTORY, MIXINS, IS_MUTABLE, IS_CONSTANT}
        or self.meta.owner_class != history_dict[OWNER_CLASS]):
        raise_unvalide_history_import_file()

    # 2. Validace historie
    history_list = history_dict[HISTORY]
    for snapshot in history_list:
        if (not isinstance(snapshot, tuple)
            or len(snapshot) != 2
            or isinstance(snapshot[0], datetime)
            or isinstance(snapshot[1], tuple)):
            raise_unvalid_snapshot_structure()

    # 3. Přepis historie
    _import_history(self, history_list)