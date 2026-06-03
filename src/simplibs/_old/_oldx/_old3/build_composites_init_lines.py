# Outers
from ......._types import SimpleMetaType


def build_composites_init_lines(
    meta: SimpleMetaType
) -> list[str]:
    """
    Vygeneruje řádky kódu pro inicializaci vnitřních kompozic (Nodes) v __init__.
    Postupuje od nejnižších (nejvnořenějších) po nejvyšší díky reversed().

    Vstupy pro pod-kompozice sbírá z již inicializovaných soukromých slotů konstant.
    """

    # 1. Definice kntejneru s popisem
    composite_lines = [
        "",
        "# Inicializace vnitřních kompozic (Nodes - zdola nahoru)"
    ]

    # 2. Iterace skrze kompozice (odzadu, abychom stavěli od základů k vrcholu)
    for composite_meta in reversed(meta.composites_map.values()):

        # 2.1 Definice kontejneru pro parametry
        composite_params = []

        # 2.2 Iterace skrze konstanty kompozice
        for const_name in composite_meta.constants_map.keys():

            # 2.2.1 Vytvoření a přidání parametru s hodnotu (branou z propery)
            composite_params.append(f"{const_name}=self.{const_name}")

        # 2.3 Spojení parametru kompozice
        composite_params_str = ", ".join(composite_params)

        # 2.3 Příprava proměných (pro snadnější zápis)
        attr_private = composite_meta.name_private
        instance_class_name = composite_meta.composite_class.__name__

        # 2.4 Sestavení a přidání konečného řetězce
        # Např.: self._motor = MotorInstance(vykon=self.vykon, ...)
        composite_lines.append(
            f"self.{attr_private} = {instance_class_name}({composite_params_str})"
        )

    # 3. Navrácení sezanamu s řetězci
    return composite_lines