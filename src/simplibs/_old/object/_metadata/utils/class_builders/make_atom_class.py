from inspect import Signature
from typing import Any
# Outers
from ...._types import SimpleMetaType, SimpleClassType
# Inners
from .base_class.AtomInstanceBase import AtomInstanceBase



def make_atom_class(
    owner_class: SimpleClassType
) -> type:
    """
    Externí továrna na INSTANCE třídy (ATOMIC).
    Vytváří fasádu, která drží CORE jádro pod specifickým jménem.
    """
    meta: SimpleMetaType = owner_class.meta

    # Příprava dat
    attr_name: str = meta.name_private
    param_name: str = meta.name_snake
    init_signature: Signature = Signature([meta.atom_param])
    core_class: type = meta.core_class

    # 1. Definice inicializačního procesu
    # noinspection PyArgumentList
    def __init__(self, param_name = None):

        # 1.1 Vyzvednutí hodnoty z kwargs
        value = kwargs.get(param_name)

        # 1.2 Vytvoření CORE instance
        setattr(self, attr_name, core_class(value))

        # 1.3 Předání zbylích kwargs dále dle MRO
        super(type(self), self).__init__(**kwargs)

    # 1.4 Podpis pro IDE a našeptávače
    __init__.__signature__ = init_signature

    # 2. Definice geteru
    def getter(self) -> Any:
        # Vrací celý objekt CORE (umožňuje přístup k .value i k metodám/metadatům)
        return getattr(self, attr_name)

    # 3. Definice setteru
    def setter(self, new_value: Any) -> None:
        # Zápis do .value na CORE objektu
        getattr(self, attr_name).value = new_value
        # Hook pro oznámení změny (pokud InstanceBase nebo mixiny vyžadují reakci)
        self._on_update()

    # 4. Definice jména třídy
    class_name = f"{owner_class.__name__}Instance"

    # 5. Definice předka (třífy pro kteoru je value určena)
    class_parents = (AtomInstanceBase,)

    # 6. Vytvoření slovníku třídy
    class_dict = {
        '__doc__': f"ATOMIC fasáda pro {owner_class.__name__}",
        '__slots__': (attr_name,),
        '__init__': __init__,
        '__allow_instantiation__': True,
        param_name: property(getter, setter),
    }

    # 7. Vytvoření objektu třídy
    instance_class = type(class_name, class_parents, class_dict)

    # 7.1 Přiřazení signatury samotné třídě (pro maximální kompatibilitu s IDE)
    instance_class.__signature__ = init_signature

    # 8. Navrácení vytvořené třídy
    return instance_class
