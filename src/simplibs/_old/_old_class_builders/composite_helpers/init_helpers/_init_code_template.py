# Outers
from ......_types import SimpleMetaType
# Constants
INDENT = "    "


def init_code_template(
    meta: SimpleMetaType
) -> str:
    """
    Vygeneruje a zkompiluje nativní metodu __init__ pro kompozici.
    Využívá pomocné generátory pro sestavení těla a signatury.
    """

    # 1. Definice parametrů
    init_params = ', '.join(name for name in meta.constants_map.keys())

    # 2. Definice inicializace konstant
    constants = []
    for name_snake, const_meta in meta.constants_map.items():
        name_private, instance_name = const_meta.name_private, const_meta.instance_name
        constants.append(f"{INDENT}self.{name_private} = {instance_name}(self.{name_snake})")
        constants.append(f"{INDENT}self.{name_private}._owner = self")

    # 3. Definice pomocné metody pro parametry kmpozice
    def composite_params(composite_meta):
        return ", ".join(
            f"{const_name}=self.{const_name}"
            for const_name in composite_meta.constants_map.keys()
        )

    # 4. Definice inicializace kompozic
    composites = []
    for comp_meta in meta.composites_map.values():
        name_private, class_name = comp_meta.name_private, comp_meta.class_name
        params = composite_params(comp_meta)
        composites.append(f"{INDENT}self.{name_private} = {class_name}({params})")
        composites.append(f"{INDENT}self.{name_private}._owner = self")

    # 5. Definice výpočtu hlavní hodnoty
    value_params = ', '.join(
        f'{inner_meta.name_snake}=self.{inner_meta.name_private}'
        for inner_meta in meta.inners
    )

    # 7. Vytvoření a návrat řetězce pro logiku
    return "\n".join([
        f"def __init__(self, *, {init_params}):",
        f"",
        f"{INDENT}# Inicializace vnitřních konstant",
        *constants,
        f"",
        f"{INDENT}# Inicializace vnitřních kompozic",
        *composites,
        f"",
        f"{INDENT}# Výpočet hodnoty třídy",
        f"{INDENT}self._value = self.calculate_value({value_params})",
    ])




