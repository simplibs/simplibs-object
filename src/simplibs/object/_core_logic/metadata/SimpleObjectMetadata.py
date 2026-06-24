from typing import Any
from functools import reduce
from operator import or_
from simplibs.sentinels import EMPTY, UNSET
# Inners
from .SimpleConstantMetadata import SimpleConstantMetadata
from .instance_builders.composite_class import make_composite_class
from .init_processors.methods import process_classmethod
from .init_processors.attributes import (
    process_type, process_inners, raise_default_is_defined_in_composition
)


# noinspection PyAttributeOutsideInit
class SimpleObjectMetadata(SimpleConstantMetadata):
    """
    Orchestrátor pro kompozitní objekty (Nodes).
    Zajišťuje propojení vnitřních prvků (inners), definici výpočetní
    logiky a správu transformačních signatur.
    """

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = (

        # 1. Data předaná uživatelem
        "inners",               # Seznam/Mapa vnitřních prvků
        "logic",                # Metoda _logic pro výpočet jádra
        "decompose",            # Metoda _decompose pro rozklad

        # 2. Mapy pro inners prvky
        "inners_params_name",   # tuple[str, ...] -> Pro bleskové mapování *args na jména
        "inners_map",           # dict[str, SimpleClassType] -> Pro všechno ostatní!

        # 3. Veřejné rozhraní
        "is_decomposeable",     # Bool parametr definující zda je možné měnit hodnotu instance rozkladem

        # 4. Cache pro instanční třídu
        "_composite_class_mutable",
        "_composite_class_immutable"
    )

    #--- Definice logiky pro inicializaci dat ---#
    # (metoda je spuštěna v initu základní třídy)
    def _process_user_data(self):

        # 1. Deklarace že třída není konstanta
        self.is_constant = False

        # 2. Zpracování _default (na kompozici nesmí být definován)
        if hasattr(self.owner_class.__dict__, "_default"):
            raise_default_is_defined_in_composition(self.owner_class)

        # 3. Zpracování _type
        (self.value_type,
         self.value_type_name) = process_type(
            owner_class=self.owner_class
        )

        # 4. Zpracování _inners
        (self.inners,
         self.node_names_set) = process_inners(
            node_names_set=self.node_names_set,
            name_snake=self.name_snake,
            owner_class=self.owner_class
        )

        # 5. Vytvoření maperů a dat pro zpracvování metohod
        self.inners_map = {inner.meta.name_snake: inner for inner in self.inners}
        self.inners_params_name = tuple(inner.meta.name_snake for inner in self.inners)

        # 6. Příprava dat pro zpracování logik
        inners_default = tuple(inner.meta.default for inner in self.inners)
        inners_annotations = {
            inner.meta.name_snake: inner.meta.value_type
            for inner in self.inners
        }

        # 7. Zpracování _logic
        (self.logic,
         self.default) = process_classmethod(
            method_name="_logic",
            expected_params=("cls", *self.inners_params_name),
            expected_args_params_count=1+len(self.inners_params_name),
            expected_args_defaults=inners_default,
            expected_kwargs_defaults={},
            expected_param_types=inners_annotations,
            expected_return_type=self.value_type,
            owner_class=self.owner_class,
            return_calculated_value=True
        )

        # 8. Zpracování _decompose
        self.decompose = process_classmethod(
            method_name="_decompose",
            expected_params=("cls", "value"),
            expected_args_params_count=2,
            expected_args_defaults=(self.default,),
            expected_kwargs_defaults={},
            expected_param_types={"value": self.value_type},
            expected_return_type=reduce(or_, inners_annotations.values()),
            owner_class=self.owner_class,
        )

        # 9. Definice rozložitelnosti
        self.is_decomposeable = (
            self.decompose is not UNSET and
            all(inner.meta.is_constant or inner.meta.is_decomposeable
                for inner in self.inners)
        )

        # 10. Zpracování _validate
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

        # 11. Příprava cache
        self._atom_class_mutable = UNSET
        self._atom_class_immutable = UNSET
        self._composite_class_mutable = UNSET
        self._composite_class_immutable = UNSET


    #--- Definice property pro výpočet a cache ---#
    # (vrací atomický základ pro třídu na instance)
    @property
    def composite_class_mutable(self):
        """Lazy brána k atomické instanci parametru."""
        if self._composite_class_mutable is EMPTY:
            self._composite_class_mutable = make_composite_class(self.owner_class.__metadata__)
        return self._composite_class_mutable

    @property
    def composite_class_immutable(self):
        """Lazy brána k atomické instanci parametru."""
        if self._composite_class_immutable is EMPTY:
            self._composite_class_immutable = make_composite_class(self.owner_class.__metadata__, mutable=False)
        return self._composite_class_immutable