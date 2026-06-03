from typing import Callable
# Outers
from ....._types import SimpleMetaType
# Inners
from .init_helpers.init_exec_code import init_exec_code
# Constants
INDENT = "    "


def create_composite_init(
    meta: SimpleMetaType
) -> Callable:
    """
    Vygeneruje a zkompiluje nativní metodu __init__ pro kompozici.
    Využívá pomocné generátory pro sestavení těla a signatury.
    """

    # 1. Získání kodu metody
    __init__ = init_exec_code(meta)

    # 2. Definice jména metody
    __init__.__name__ = "__init__"

    # 3. Definice qualname
    __init__.__qualname__ = f"{meta.class_name}.__init__"

    # 4. Definice docstringu metody
    init_args_lines = []
    for name, const_meta in meta.constants_map.items():
        param_type = const_meta.value_type
        type_name = param_type.__name__ if hasattr(param_type, '__name__') else str(param_type)
        init_args_lines.append(f"{INDENT}{name} ({type_name}): Konstantní hodnota pro kompozice.")
    init_args_block = "\n".join(init_args_lines)

    __init__.__doc__ = (
        f"Inicializuje kompozitní instanci {meta.class_name}.\n"
        f"\n"
        f"Tato metoda nastavuje výchozí stav vnitřních konstant a z nich automaticky\n"
        f"dopočítává hodnoty vnitřních kompozic a hlavní hodnotu této třídy.\n\n"
        f"Poznámka:\n"
        f"{INDENT}Přímé nastavení nebo změna hodnot celých sub-kompozic se provádí až na\n"
        f"{INDENT}inicializovaném objektu skrze property, a to pouze v případě, že jsou\n"
        f"{INDENT}definované příslušné metody pro rozklad (decomposition) hodnoty.\n"
        f"\n"
        f"Args:\n"
        f"{init_args_block}"
    )

    # 5. Definice defaultních hodnot pro kwargs
    __init__.__kwdefaults__ = {
        name: const_meta.default
        for name, const_meta in meta.constants_map.items()
    }

    # 6. Definice anotací (návratové hodnoty)
    __init__.__annotations__ = {
        name: const_meta.value_type
        for name, const_meta in meta.constants_map.items(),
    } | {"return": None}

    # 6. Navrácení zpracované metody
    return __init__
