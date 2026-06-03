from inspect import Signature
from typing import Any
# Outers
from .AtomInstanceBase import AtomInstanceBase


def make_atom_instance_class(base_class: type) -> type:
    """
    Externí továrna na INSTANCE třídy (ATOMIC).
    Vytváří fasádu, která drží CORE jádro pod specifickým jménem.
    """

    # Příprava dat
    attr_name = base_class.meta.name_private  # např. _auto
    param_name = base_class.meta.name_snake  # např. auto
    atom_param_signature = base_class.meta.atom_param_signature
    init_signature = Signature([atom_param_signature])
    CoreClass = base_class.CORE()

    # 1. Definice inicializačního procesu
    # noinspection PyArgumentList
    def __init__(self, **kwargs):

        # 1.1 Vyzvednutí hodnoty z kwargs
        value = kwargs.get(param_name)

        # 1.2 Vytvoření CORE instance
        setattr(self, attr_name, CoreClass(value))

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
        if hasattr(self, '_on_update'):
            self._on_update()

    # 4. Definice jména třídy
    class_name = f"{base_class.__name__}Instance"

    # 5. Definice předka (třífy pro kteoruje value určena)
    class_parents = (AtomInstanceBase,)

    # 6. Vytvoření slovníku třídy
    class_dict = {
        '__doc__': f"ATOMIC fasáda pro {base_class.__name__}",
        '__slots__': (attr_name,),
        '__init__': __init__,
        param_name: property(getter, setter),
    }

    # 7. Vytvoření objektu třídy
    instance_class = type(class_name, class_parents, class_dict)

    # 7.1 Přiřazení signatury samotné třídě (pro maximální kompatibilitu s IDE)
    instance_class.__signature__ = init_signature

    return instance_class
