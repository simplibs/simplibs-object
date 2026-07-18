from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleBaseMetadata import SimpleBaseMetadata
from .instance_builders.atom_class import make_atom_class
from .init_processors.methods import process_classmethod
from .init_processors.attributes import (
    process_type, process_default_for_constant
)
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleConstantMetadataProtocol
    from ...protocols.instance.core_classes import AtomInstanceProtocol


# noinspection PyAttributeOutsideInit
class SimpleConstantMetadata(SimpleBaseMetadata):
    """
    Specializovaný orchestrátor pro konstanty (Atomy).
    Zajišťuje, že každý list systému má jasně definovaný typ,
    validní výchozí hodnotu a funkční validační rozhraní.
    """

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = (

        # 1. Data předaná uživatelem
        "value_type",       # Normalizovaný typ (_type)
        "default",          # Výchozí hodnota (_default)
        "validate",         # Reference na metodu _validate

        # 2. Veřejné rozhraní
        "value_type_name",  # Jméno typu (str)
        "is_constant",      # Bool parametr definující zda jde o konstantu

        # 3. Cache pro instanční třídu
        "_atom_class_mutable",
        "_atom_class_immutable"
    )

    #--- Definice logiky pro inicializaci dat ---#
    # (metoda je spuštěna v initu základní třídy)
    def _process_user_data(
        self: "SimpleConstantMetadataProtocol"
    ) -> None:

        # 1. Deklarace že třída je konstanta
        self.is_constant = True

        # 2. Zpracování _type
        (self.value_type,
         self.value_type_name) = process_type(
            owner_class=self.owner_class
        )

        # 3. Zpracování _default
        self.default = process_default_for_constant(
            default_type=self.value_type,
            owner_class=self.owner_class
        )

        # 4. Zpracování _validate
        self.validate = process_classmethod(
            method_name="_validate",
            expected_params=("cls", "value", "return_bool"),
            expected_args_params_count=2,
            expected_args_defaults=(),
            expected_kwargs_defaults={"return_bool": False},
            expected_param_types={"value": Any, "return_bool": bool},
            expected_return_type=bool | None,
            test_value=(self.default,),
            owner_class=self.owner_class,
        )

        # 5. Příprava cache
        self._atom_class_mutable = UNSET
        self._atom_class_immutable = UNSET

    #--- Definice property pro výpočet a cache ---#
    # (vrací atomický základ pro třídu na instance)
    @property
    def atom_class_mutable(
        self: "SimpleConstantMetadataProtocol"
    ) -> "AtomInstanceProtocol":
        """Lazy brána k core instanci parametru."""
        if self._atom_class_mutable is UNSET:
            self._atom_class_mutable = make_atom_class(self.owner_class.__metadata__)
        return self._atom_class_mutable

    @property
    def atom_class_immutable(
        self: "SimpleConstantMetadataProtocol"
    ) -> "AtomInstanceProtocol":
        """Lazy brána k core instanci parametru."""
        if self._atom_class_immutable is UNSET:
            self._atom_class_immutable = make_atom_class(self.owner_class.__metadata__, mutable=False)
        return self._atom_class_immutable

