from typing import Any
from functools import reduce
from operator import or_
from simplibs.sentinels import EMPTY
# Inners
from ._SimpleConstantMetadata import SimpleConstantMetadata
from .processors.attributes import process_type, process_inners, process_default_for_composition
from .processors.methods import process_classmethod
from .utils.class_builders import make_composite_class
from .utils.param_builders import collect_composite_params


# noinspection PyAttributeOutsideInit
class SimpleObjectMetadata(SimpleConstantMetadata):
    """
    Orchestrátor pro kompozitní objekty (Nodes).
    Zajišťuje propojení vnitřních prvků (inners), definici výpočetní
    logiky a správu transformačních signatur.
    """

    __slots__ = (
        # Definice struktury
        "inners",  # Seznam/Mapa vnitřních prvků
        "logic",  # Metoda _logic pro výpočet jádra
        "decompose",  # Metoda _decompose pro rozklad

        # Signatury (Rozhraní)
        "logic_signature",  # Parametry pro metodu _logic
        "decompose_signature",  # Parametry pro metodu _decompose

        # Cache pro dynamické objekty (rozšířená o mixiny)
        "_composite_params",
        "_composite_class",
    )

    def _process_user_interface(self):

        # 1. Definice bool parametrů
        self.is_constant = False
        self.is_user_code = True

        # 2. Zpracování _type
        self.value_type = process_type(
            owner_class=self.owner_class
        )

        # 3. Zpracování _inners
        (self.inners,
         self.used_names,
         inners_params_name,
         inners_default,
         inners_annotations) = process_inners(
            used_names=self.used_names,
            name_snake=self.name_snake,
            owner_class=self.owner_class
        )

        # 4. Zpracování _logic
        (self.logic,
         logic_calculated_value) = process_classmethod(
            method_name="_logic",
            expected_params=("cls", *inners_params_name),
            expected_args_params_count=1,
            expected_args_defaults=None,
            expected_kwargs_defaults=inners_default,
            expected_param_types=inners_annotations,
            expected_return_type=self.value_type,
            owner_class=self.owner_class,
            return_calculated_value=True
        )

        # 5. Zpracování _decompose
        self.decompose = process_classmethod(
            method_name="_decompose",
            expected_params=("cls", "value"),
            expected_args_params_count=2,
            expected_args_defaults=(logic_calculated_value,),
            expected_kwargs_defaults={},
            expected_param_types={"value": self.value_type},
            expected_return_type=reduce(or_, inners_annotations.values()),
            owner_class=self.owner_class,
        )

        # 6. Zpracování _validate
        self.validate = process_classmethod(
            method_name="_validate",
            expected_params=("cls", "value", "return_bool"),
            expected_args_params_count=2,
            expected_args_defaults=None,
            expected_kwargs_defaults={"return_bool": False},
            expected_param_types={"value": Any, "return_bool": bool},
            expected_return_type=bool | None,
            test_value=(logic_calculated_value,),
            owner_class=self.owner_class,
        )

        # 7. Zpracování _default
        (self.default,
         self.logic,
         self.decompose,
         self.validate) = process_default_for_composition(
            calculate_default=logic_calculated_value,
            default_type=self.value_type,
            logic_method=self.logic,
            decompose_method=self.decompose,
            validate_method=self.validate,
            owner_class=self.owner_class
        )

    def _prepare_cache_attributes(self):
        """Inicializace cache slotů do výchozího stavu."""
        # 1. Načtení nastavení z SimpleConstantMetadata
        super()._prepare_cache_attributes()

        # 2. Přidání dalších položek
        self._composite_params = EMPTY
        self._composite_class = EMPTY


    @property
    def composite_params(self):
        """Lazy brána k signatuře parametru."""
        if self._composite_params is EMPTY:
            self._composite_params = collect_composite_params(self.owner_class)
        return self._composite_params

    @property
    def composite_class(self):
        """Lazy brána k atomické instanci parametru."""
        if self._composite_class is EMPTY:
            self._composite_class = make_composite_class(self.owner_class)
        return self._composite_class