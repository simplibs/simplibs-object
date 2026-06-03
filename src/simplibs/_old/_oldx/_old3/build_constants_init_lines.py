# Outers
from ......._types import SimpleMetaType


def build_constants_init_lines(
    meta: SimpleMetaType
) -> list[str]:
    """
    Vygeneruje řádky kódu pro inicializaci vnitřních konstant (atomů) v __init__.
    Instance se ukládají přímo do soukromých slotů a jméno třídy berou z jejích metadat.
    """

    # 1. Definice kntejneru s popisem
    constant_lines = [
        "",
        "# Inicializace vnitřních konstant (Atomy)"
    ]

    # 2. Iterace skrze konstanty
    for name_snake, const_meta in meta.constants_map.items():

        # 2.1 Příprava proměných (pro snadnější zápis)
        attr_private = const_meta.name_private
        instance_class_name = const_meta.atom_class.__name__

        # 2.2 Sestavení a přidání konečného řetězce
        # Např.: self._cena = CenaInstance(self.cena)
        constant_lines.append(
            f"self.{attr_private} = {instance_class_name}(self.{name_snake})"
        )

    # 3. Navrácení sezanamu s řetězci
    return constant_lines

