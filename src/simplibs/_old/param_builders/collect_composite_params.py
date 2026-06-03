import inspect
from typing import List
# Outers
from ...._types import SimpleMetaType, SimpleClassProtocol

def collect_composite_params(
    owner_class: SimpleClassProtocol
) -> List[inspect.Parameter]:
    """
    Rekurzivně sbírá parametry ze všech inners napříč celou strukturou.
    Využívá lazy property metadat pro maximální výkon.
    """
    meta: SimpleMetaType = owner_class.meta

    # 1. Začneme vlastním parametrem (to, co definuje tento uzel)
    # Voláme .atom_params, což v SimpleConstantMetadata
    # spustí tu naši lazy výrobu signatury.
    parameters = [meta.atom_param]

    # 2. Projdeme všechny vnořené prvky (inners)
    # Pokud je inners UNSET nebo prázdný, rekurze se zde přirozeně zastaví.
    inners = getattr(meta, 'inners', [])

    for inner in inners:
        # Rekurzivně voláme tuto funkci na vnořenou třídu.
        # Výsledkem je, že probubláme až k nejhlubším atomům.
        parameters.extend(collect_composite_params(inner))

    return parameters