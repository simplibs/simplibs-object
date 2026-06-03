from inspect import Signature
from typing import Any, Callable
# Outers
from ...._types import SimpleMetaType, SimpleClassProtocol
# Inners
from .base_class.AtomInstanceBase import AtomInstanceBase

def make_atom_init(
    owner_class: SimpleClassProtocol
) -> Callable:
    """
    Dynamicky vytvoří inicializační metodu
    pro ATOMIC instance třídu.
    """

    # Metadata
    meta: SimpleMetaType = owner_class.meta

    # Data
    attr_name = meta.name_private
    param_name = meta.name_snake
    param_type = meta.value_type
    core_class = meta.core_class
    class_name = owner_class.__name__

    # Source
    source = dedent(f'''
    def __init__(
        self,
        {param_name}: param_type | None = None
    ) -> None:
        """
        Inicializační metoda pro třídu {class_name}.
        """

        self.{attr_name} = core_class({param_name})
    ''')

    # Namespace
    namespace = {
        "param_type": param_type,
        "core_class": core_class,
    }

    # Compile
    exec(source, namespace)

    # Return function
    return namespace["__init__"]

def make_atom_class(
    owner_class: SimpleClassProtocol
) -> type:
    """
    Externí továrna na INSTANCE třídy (ATOMIC).
    Vytváří fasádu, která drží CORE jádro pod specifickým jménem.
    """

    # 1. Příprava dat
    meta: SimpleMetaType = owner_class.meta
    attr_name = meta.name_private
    param_name = meta.name_snake

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
        '__init__': make_atom_init(owner_class),
        '__allow_instantiation__': True,
        param_name: property(getter, setter),
    }

    # 7. Vytvoření objektu třídy
    return type(class_name, class_parents, class_dict)

