from inspect import Signature
from typing import Any


def make_instance_class(cls):
    """
    Externí továrna na INSTANCE třídy (ATOMIC).
    Vytváří fasádu, která drží CORE jádro pod specifickým jménem.
    """

    # Příprava názvů a třídy jádra z metadat
    # Předpokládáme, že cls.CORE() vrací už nacachovanou CoreClass
    attr_name = cls.meta.name_private  # např. _auto
    param_name = cls.meta.name_snake  # např. auto
    CoreClass = cls.CORE()  # Třída vytvořená pomocí make_core_class

    # 1. Konstruktor
    def __init__(self, **kwargs):
        # Vyzvedneme hodnotu z kwargs podle snake_name (např. auto='Škoda')
        value = kwargs.get(param_name)

        # Vytvoříme instanci CORE a uložíme ji do privátního atributu
        # CoreClass(value) v sobě automaticky spustí normalize(process_none=True)
        setattr(self, attr_name, CoreClass(value))

        # Posuneme zbylé kwargs dál v MRO (klíčové pro kompozice)
        super(type(self), self).__init__(**kwargs)

    # 2. Getter pro veřejné rozhraní
    def getter(self):
        # Vrací celý objekt CORE (umožňuje přístup k .value i k metodám/metadatům)
        return getattr(self, attr_name)

    # 3. Setter pro veřejné rozhraní
    def setter(self, value):
        # Zápis do .value na CORE objektu spustí jeho vnitřní setter (včetně kontroly mutable)
        # Tím pádem zde nemusíme znovu řešit, zda je třída mutable nebo ne.
        getattr(self, attr_name).value = value

        # Hook pro oznámení změny (pokud InstanceBase nebo mixiny vyžadují reakci)
        if hasattr(self, '_on_update'):
            self._on_update()

    # 4. Sestavení třídy
    class_name = f"{cls.__name__}Instance"

    # InstanceBase je lehký základ, který zajistí, že třída nemá zbytečné předky ze SimpleBase
    class_parents = (InstanceBase,)

    class_dict = {
        '__doc__': f"ATOMIC fasáda pro {cls.__name__}",
        '__slots__': (attr_name,),
        '__init__': __init__,
        # Dynamicky pojmenovaná property (např. auto)
        param_name: property(getter, setter),
    }

    # Dynamické vytvoření třídy
    instance_class = type(class_name, class_parents, class_dict)

    # Přidání podpisu pro IDE (aby našeptávalo správné parametry v __init__)
    instance_class.__init__.__signature__ = Signature([cls.meta.atom_param_signature])

    return instance_class



