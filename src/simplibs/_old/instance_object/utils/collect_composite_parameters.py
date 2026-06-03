import inspect
from typing import List


def collect_composite_parameters(cls: type) -> List[inspect.Parameter]:
    """
    Rekurzivně sbírá parametry ze všech inners.
    """
    # 1. Začneme vlastním parametrem (atomem)
    parameters = [cls.meta.atom_param]

    # 2. Pokud jsou inners, projdeme je
    # Používáme hasattr nebo kontrolu UNSET, abychom předešli chybám u čistých atomů
    inners = getattr(cls.meta, 'inners', [])
    if inners:
        for inner in inners:
            # Rekurzivní volání stejné funkce
            # Předpokládáme, že i inners mají přístup k této logice nebo metadatům
            parameters.extend(collect_composite_parameters(inner))

    return parameters