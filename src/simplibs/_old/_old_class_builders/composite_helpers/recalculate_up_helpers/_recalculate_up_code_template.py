# Outers
from ......_types import SimpleMetaType
# Constants
INDENT = "    "

def recalculate_up_code_template(
    meta: SimpleMetaType
) -> str:
    """
    Vygeneruje optimalizovaný kód metody pro přepočet hodnoty kompozice směrem nahoru.
    """

    # 1. Definice parametrů
    value_params = ', '.join(
        f'{inner_meta.name_snake}=self.{inner_meta.name_private}.value'
        for inner_meta in meta.inners
    )

    # 2. Vytvoření a navrácení finálníto řetězce
    return "\n".join([
        f"def _recalculate_up(self) -> None:",
        f"{INDENT}# 1. Přímý výpočet nové hodnoty z vnitřních slotů",
        f"{INDENT}new_value = self.calculate_value({value_params})",
        f"",
        f"{INDENT}# 2. Zápis a propagace pouze při reálné změně",
        f"{INDENT}if self._value != new_value:",
        f"{INDENT}{INDENT}self._value = new_value",
        f"",
        f"{INDENT}{INDENT}# 3. Pokud mě vlastní jiná kompozice, předáme update výše",
        f"{INDENT}{INDENT}if self._owner is not None:",
        f"{INDENT}{INDENT}{INDENT}self._owner._recalculate_up()",
    ])
