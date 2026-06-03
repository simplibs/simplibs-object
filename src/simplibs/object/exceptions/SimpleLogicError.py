from .SimpleError import SimpleError

class SimpleLogicError(SimpleError):
    """Výjimka pro chyby vzniklé při manipulaci s daty (validace, tvorba, update)."""

_DESIGN_NOTES = """
# SimpleLogicError

## Účel
Tato výjimka pokrývá celý životní cyklus dat uvnitř SimpleObjectu. Vyvolává se v momentě, 
kdy jsou metadata v pořádku, ale konkrétní data (hodnoty) nevyhovují pravidlům.

## Logika
Dědí z `SimpleError`. Používá se v mixinech `base_logic` pro:
- Selhání typové kontroly (ValidateType).
- Selhání uživatelské validace (Validate).
- Chyby při normalizaci (Normalize).
- Problémy při dekompozici nebo skládání hodnoty (Create/Update/Decompose).

## Poznámky
Oddělením od `SimpleMetadataError` dáváme uživateli jasný nástroj, jak 
rozlišit mezi špatně napsaným kódem (třídou) a špatně zadanými daty (instancí).
"""