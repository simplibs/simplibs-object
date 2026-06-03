from typing import Callable
# Outers
from ......_types import SimpleMetaType
# Inners
from ._recalculate_up_code_template import recalculate_up_code_template


def recalculate_up_code(
    meta: SimpleMetaType
) -> Callable:
    """
    Zkompiluje textovou šablonu _recalculate_up do podoby spustitelné funkce.
    """
    # 1. Získání textového zdrojového kódu
    source_code = recalculate_up_code_template(meta)

    # 2. Příprava lokálního kontextu, do kterého exec metodu "vystřelí"
    local_namespace = {}

    # 3. Kompilace a spuštění kódu v izolovaném prostoru
    # exec vytvoří v local_namespace klíč '_recalculate_up' s hotovou funkcí
    exec(source_code, {}, local_namespace)

    # 4. Vytažení a návrat definice kodu initu z local_namespace
    return local_namespace["_recalculate_up"]
