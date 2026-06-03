from typing import Type, Any, Dict, Tuple
from simplibs.sentinels import UNSET
# Outers
from .._types import SimpleClassType, SimpleMetaType, SimpleClassType
# Inners
from .SimpleConstantMetadata import SimpleConstantMetadata
from .SimpleObjectMetadata import SimpleObjectMetadata
from .validations import raise_frozen_attribute_error, validate_mixins, validate_bool
from .constants import BASE_CLASS_NAMES
from .utils.base_class_utils import create_simple_instance


class SimpleMeta(type):
    """
    Metatřída systému Simple. Zajišťuje automatickou orchestraci metadat
    při definici třídy a chrání integritu jejího rozhraní.
    """

    #--- Metoda pro vytvoření třídy ---#
    # (u defiičních tříd vytváří metadata)
    def __new__(
        mcls: SimpleClassType,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> SimpleClassType:
        """
        Analyzuje vznikající třídu a rozhoduje o jejím zařazení (Kořen/Konstanta/Kompozice).
        """

        # 1. Vytvoření objektu třídy
        cls = super().__new__(mcls, name, bases, namespace)

        # 2. Přeskočení vytváření metadata pro základní a instanční třídy
        if hasattr(cls, "_is_instance_class") or name in BASE_CLASS_NAMES:
            return cls

        # 3. Výpočet metadat (pro deklarativní třídy)
        cls.__metadata__ = (
            SimpleObjectMetadata(owner_class=cls)
            if hasattr(cls, "_inners")
            else SimpleConstantMetadata(owner_class=cls)
        )

        # 4. Navrácení třídy
        return cls

    #--- Metoda pro zápis atributů hlavní třídy ---#
    # (zamezuje přepisu již zadaných dat)
    def __setattr__(
        cls,
        attr_name: str,
        new_value: Any
    ) -> None:
        """Definice setteru znemožnující přepis již zapsaných hodnot."""

        # 1. Kontrola zda nedochází k přepisu atributu
        if getattr(cls, attr_name, UNSET) is not UNSET:
            raise_attribut_allready_set(cls, attr_name, new_value)

        # 2. Zápis hodnoty
        super().__setattr__(attr_name, new_value)

    #--- Metoda pro vytváření instancí ---#
    # (dopočítá instanční třídu a vrátí instanci)
    def __call__(cls, mixins: tuple = (), as_atom: bool = False):
        """
        Zachycuje volání Auto(mixins).
        Třída Auto se zde chová čistě jako recept/funkce.
        """
        # if cls.__name__ in BASE_CLASS_NAMES:
        #     raise TypeError(
        #         f"Systémovou bázi '{cls.__name__}' nelze přímo instanciovat. "
        #         "Použij ji jako předka pro svou vlastní třídu."
        #     )

        # 1. Validace vstupních dat
        validate_class_not_base_class(cls)
        validate_mixins(mixins)
        validate_bool(as_atom)

        # 2. Získání základní třídy
        is_atom = cls.meta.is_constant or as_atom
        base_class = cls.meta.atom_class if is_atom else cls.meta.composite_class

        # 3. Sestavení instanční třídy
        class_parents = (*mixins, base_class)
        class_name = f"{cls.meta.class_name}Instance"
        class_dict = {"__slots__": ()}
        _instance_cls = type(class_name, class_parents, class_dict)
        _instance_cls.__qualname__ = class_name

        # 3. Vytvoření instance
        # noinspection PyTypeChecker
        instance = object.__new__(_instance_cls)
        # noinspection PyArgumentList
        return instance.__init__()

    #--- Property usnadňující přístup k metadatům ---#
    # (pro tuto třídu)
    @property
    def meta(cls) -> SimpleMetaType:
        """Veřejné rozhraní pro přístup k metadatům třídy."""
        return cls.__metadata__

    # --- Definice __repr__ pro definiční třídy ---#
    def __repr__(cls) -> str:
        """
        Technická reprezentace samotné definiční třídy (šablony).
        Ukazuje typ blueprintu a informaci, zda jde o Konstantu nebo Kompozici.
        """
        # Pokud jsme na systémové bázi, která ještě nemá metadata
        if cls.meta is UNSET:
            return f"<class {cls.__name__} (System Base)>"

        type_kind = "Constant" if cls.meta.is_constant else "Object"
        return f"<{cls.meta.class_name}Blueprint blueprint='{cls.meta.blueprint}' type={type_kind}>"

    # --- Definice __str__ pro definiční třídy ---#
    def __str__(cls) -> str:
        """
        Uživatelská reprezentace třídy.
        Vrací čisté byznysové jméno třídy.
        """
        if cls.meta is UNSET:
            return cls.__name__

        return cls.meta.class_name