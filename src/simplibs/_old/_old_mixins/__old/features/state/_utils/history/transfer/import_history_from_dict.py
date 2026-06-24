from datetime import datetime
# Outers
from ......_constants import OWNER_CLASS, HISTORY
from .._validations import raise_unvalid_snapshot_structure, raise_unvalide_history_import_file
# Inners
from ._import_history import _import_history


def import_history_from_dict(self, history_dict: dict):
    """Importuje historii z přenositelného formátu s kontrolou owner_class."""

    # 1. Validace kontejneru
    if (not isinstance(history_dict, dict) and
        len(history_dict) != 2 and
        set(history_dict.keys()) == {OWNER_CLASS, HISTORY} and
        self.meta.owner_class != history_dict[OWNER_CLASS]):
        raise_unvalide_history_import_file()

    # 2. Validace historie
    history_list = history_dict[HISTORY]
    for snapshot in history_list:
        if (not isinstance(snapshot, tuple) and
            len(snapshot) != 2 and
            isinstance(snapshot[0], datetime) and
            isinstance(snapshot[1], tuple)):
            raise_unvalid_snapshot_structure()

    # 3. Přepis historie
    _import_history(self, history_list)