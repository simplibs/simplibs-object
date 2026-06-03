from typing import Callable
# Outers
from ......_types import SimpleMetaType
# Inners
from ._init_code_template import init_code_template


def init_code(
    meta: SimpleMetaType
) -> Callable:
    """
    Vygeneruje a zkompiluje nativní metodu __init__ pro kompozici.
    Využívá pomocné generátory pro sestavení těla a signatury.
    """

    # 1. Vytvoření defnice kodu
    code_string = init_code_template(meta)

    # 2. Příprava lokálního kontextu pro exec
    local_namespace = {}

    # 3. Zpřístupníme instanční třídy pro všechny konstanty
    for const_meta in meta.constants_map.values():
        local_namespace[const_meta.atom_class.__name__] = const_meta.atom_class

    # 4. Zpřístupníme instanční třídy pro všechny vnitřní kompozice
    for comp_meta in meta.composites_map.values():
        local_namespace[comp_meta.composite_class.__name__] = comp_meta.composite_class

    # 5. Spuštění exec (zkompilování stringu do živého kódu)
    exec(code_string, {}, local_namespace)

    # 6. Vytažení a návrat definice kodu initu z local_namespace
    return local_namespace["__init__"]


