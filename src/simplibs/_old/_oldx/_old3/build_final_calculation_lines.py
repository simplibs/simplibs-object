# Outers
from ......._types import SimpleMetaType


def build_final_calculation_lines(
    meta: SimpleMetaType
) -> list[str]:
    """
    Vygeneruje finální řádky pro __init__ kompozice.
    Vypočítá celkovou hodnotu '_value' pomocí metody _logic a provede normalizaci.
    """

    # 1. Definice kontejneru pro parametry
    logic_args = []

    # 2. Cyklus skrze inners (pro získání parametrů)
    for inner_meta in meta.inners:

        # 2.3 Příprava proměných (pro snadnější zápis)
        name_snake = inner_meta.name_snake
        attr_private = inner_meta.name_private

        # 2.4 Sestavení a přidání konečného řetězce
        # Např.: vykon=self.vykon
        logic_args.append(
            f"{name_snake}=self.{name_snake}"
        )

    # 3. Spojení parametrů
    logic_args_str = ", ".join(logic_args)

    # 4. Defince a navrácení seznamu s řetězci
    return [
        "",
        "# Výpočet celkové hodnoty kompozice",
        f"self.value = self.calculate_value({logic_args_str})",
    ]