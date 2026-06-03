from .SimpleObjectError import SimpleObjectError

class SimpleObjectMetadataError(SimpleObjectError):
    """Výjimka pro chyby v definici metadat a struktuře SimpleObject tříd."""


_DESIGN_NOTES = """
# SimpleObjectMetadataError

## Účel
Skupinová výjimka pro chyby vzniklé při deklaraci a validaci tříd. 
Dědí z `SimpleObjectError`, takže ji lze zachytit i skrze ni.

## Logika
Tato výjimka se typicky vyvolává v rámci metatřídy a orchestrátoru metadat. 
Indikuje, že uživatel špatně definoval svou třídu (např. chybný název, typ nebo inners).
"""