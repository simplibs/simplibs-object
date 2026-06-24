# Outers
from ...._types import SimpleMetaType


def build_recursive_maps(
    meta: SimpleMetaType
) -> tuple[dict[str, SimpleMetaType], ...]:

    # 1. Vytvoření prázdných slovníků
    constants = {}
    composites = {}

    # 2. Funkce pro rekurzivní zběr
    def walk(m):

        # 2.1 Průchod zkrze inners
        for inner in m.inners:

            # 2.1.1 Vyřízení konstanty
            if inner.meta.is_constant:
                constants[inner.meta.name_snake] = inner.meta

            # 2.1.2 Vyžízení kompozice (rekurzivní volání)
            else:
                composites[inner.meta.name_snake] = inner.meta
                walk(inner.meta)

    # 3. Zpuštění rekurze
    walk(meta)

    # 4. Návrat slovníků
    return constants, composites