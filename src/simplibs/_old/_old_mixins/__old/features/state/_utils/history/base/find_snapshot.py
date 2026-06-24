from datetime import datetime
# Outers
from .._validations import (
    raise_unvalide_snapshot_index,
    raise_unvalide_timestamp,
    raise_unvalide_snopshot_timestamp,
    raise_unvalide_snopshot_reference
)


def find_snapshot(self, ref) -> tuple:
        """Převede index nebo timestamp na snapshot."""

        # 1. Zpracování int hodnoty
        if isinstance(ref, int):

            # 1.1 Validace zadané hodnoty
            if not (0 <= ref < self._history_count):
                raise_unvalide_snapshot_index()

            # 1.2 Navrácení snapshotu
            return self._history[ref][1]

        # 2. Zpracování datetime hodnoty
        if isinstance(ref, datetime):

            # 2.1 Validace zadané hodnoty
            if not isinstance(ref, datetime):
                raise_unvalide_timestamp()

            # 2.2 Navrácení snapshotu
            for ts, snapshot in self._history:
                if ts == ref:
                    return snapshot

            # 2.3 Výjimky když nebyl timestamp nalezen
            raise_unvalide_snopshot_timestamp()

        # 3. Vyvolání výjimky pro nevalidní vstupní hodnotu
        raise_unvalide_snopshot_reference()
        return ()  # Nikdy sem nedojdem
