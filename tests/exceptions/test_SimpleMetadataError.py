from .SimpleError import SimpleError

class SimpleMetadataError(SimpleError):
    """Výjimka pro chyby v definici metadat a struktuře SimpleObject tříd."""


_DESIGN_NOTES = """
# SimpleMetadataError

## Účel
Skupinová výjimka pro chyby vzniklé při deklaraci a validaci tříd. 
Dědí z `SimpleError`, takže ji lze zachytit i skrze ni.

## Logika
Tato výjimka se typicky vyvolává v rámci metatřídy a orchestrátoru metadat. 
Indikuje, že uživatel špatně definoval svou třídu (např. chybný název, typ nebo inners).
"""