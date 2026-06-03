import warnings
from typing import Any, Tuple, List, Optional, Union
from simplibs.exception import SimpleException
from ..mixins.object.defaults import IdentityMixin, MetadataMixin, ClonableMixin, SerializableMixin

DEFAULT_MIXINS: List[type] = [
    IdentityMixin,      # __repr__, __str__, __bool__, __hash__, __eq__
    MetadataMixin,      # meta, name_readable, name_snake, value_type, is_composite, is_atom
    ClonableMixin,      # copy, with_
    SerializableMixin   # _serialize_value, to_dict, to_json, from_dict, from_json
]

def process_mixins(*mixins: Any, use_defaults: bool =True) -> Tuple[type, ...]:
    """
    Zpracuje a validuje mixiny pro SimpleObject.
    Vrací unikátní tuple tříd připravených pro dědičnost.
    """
    # Načtení mixinů předaných uživatelem
    user_mixins = list(mixins)

    # Přidání defaultů, pokud nejsou potlačené
    if use_defaults:
        user_mixins.extend(DEFAULT_MIXINS)

    # Kontrola zda jsou všechnymixiny kompatibilní a schopné vytvořit instanci
    all_mixins_are_compatible = True
    try:
        # Pokus o vytvoření dočasného potomka pro ověření kompatibility
        type("_SimpleTestChild", (*user_mixins,), {"__slots__": ()})
    except TypeError as e:
        all_mixins_are_compatible = False


    # Zvalidované mixiny připravené na implementaci
    validated_mixins: List[type] = []

    # Procházení všech mixinů
    for mixin in user_mixins:

        # Přidáme pouze unikátní mixiny (zachováme pořadí prvního výskytu)
        if mixin not in validated_mixins:

            # Pokud neprošla kontrola kompatibility
            if not all_mixins_are_compatible:

                # 1. Musí to být třída (type)
                if not isinstance(mixin, type):
                    raise SimpleException(
                        error_name="MIXIN TYPE ERROR",
                        value_label="mixin",
                        value=type(mixin).__name__,
                        expected="A class (type), not an instance",
                        problem=f"Element '{mixin}' is not a valid class and cannot be used as a mixin.",
                        how_to_fix=(
                            "Pass the class itself (e.g., ClonableMixin).",
                            "Ensure you didn't add parentheses (e.g., ClonableMixin()) which creates an instance."
                        ),
                        context="Validation of input arguments in process_mixins",
                        exception=TypeError
                    )

                # 2. Kontrola, zda je třída použitelná pro dědičnost (Inheritance Test)
                try:
                    # Pokus o vytvoření dočasného potomka pro ověření kompatibility
                    type("_SimpleDiagnosticChild", (mixin,), {"__slots__": ()})
                except TypeError as e:
                    raise SimpleException(
                        error_name="INVALID MIXIN ERROR",
                        value_label="mixin_class",
                        value=mixin.__name__,
                        expected="A class that can be inherited from",
                        problem=f"The class '{mixin.__name__}' is not a valid base for inheritance. Error: {str(e)}",
                        how_to_fix=(
                            "Ensure the mixin is a standard class, not a built-in type like 'bool' or 'int'.",
                            "Check if the class is decorated with '@final', which prevents inheritance.",
                            "Verify there are no metaclass conflicts between this mixin and SimpleBase."
                        ),
                        context=f"Pre-inheritance compatibility check for {mixin.__name__}",
                        exception=TypeError
                    )

            # Kontrola __slots__ (Vzdělávací varování - neblokuje běh)
            if not hasattr(mixin, "__slots__"):
                warnings.warn(
                    f"Mixin '{mixin.__name__}' is missing '__slots__'. "
                    f"The resulting SimpleObject will use a '__dict__', increasing memory usage. "
                    f"Consider adding '__slots__ = ()' to the mixin definition.",
                    UserWarning,
                    stacklevel=3
                )

            validated_mixins.append(mixin)

    # Převod na tuple a návrat
    return tuple(validated_mixins)