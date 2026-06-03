from typing import Any, Dict, Tuple, Self
from simplibs.sentinels import UNSET
# Outers
from .._types import SimpleMetaType, SimpleClassType
# Inners
from .SimpleConstantMetadata import SimpleConstantMetadata
from .SimpleObjectMetadata import SimpleObjectMetadata
from .constants import BASE_CLASS_NAMES
from .validations import raise_attribut_allready_set
from .instance_builders import create_instance


class SimpleMeta(type):
    """
    Metatřída systému Simple. Zajišťuje automatickou orchestraci metadat
    při definici třídy a chrání integritu jejího rozhraní.
    """

    #--- Metoda pro vytvoření třídy ---#
    # (u defiičních tříd vytváří metadata)
    def __new__(
        mcls: Self,
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
        """Definuje zamezení přepisu již zapsaných hodnot."""

        # 1. Kontrola zda nedochází k přepisu atributu
        if getattr(cls, attr_name, UNSET) is not UNSET:
            raise_attribut_allready_set(cls, attr_name, new_value)

        # 2. Zápis hodnoty
        super().__setattr__(attr_name, new_value)


    #--- Metoda pro vytváření instancí ---#
    # (dopočítá instanční třídu a vrátí instanci)
    def __call__(cls: SimpleClassType, mixins: tuple = (), as_atom: bool = False):
        """
        Metoda pro vytváření instancí, dopočítá instanční třídu a vrátí instanci.
        """
        return create_instance(cls, mixins, as_atom)


    # --- Definice __repr__ pro definiční třídy ---#
    def __repr__(cls) -> str:
        """
        Technická reprezentace samotné definiční třídy (šablony).
        Ukazuje typ blueprintu a informaci, zda jde o Konstantu nebo Kompozici.
        """
        return (
            f"<class {cls.__name__} (System Base)>"
            if cls.meta is UNSET else
            f"<{cls.meta.class_name}Blueprint blueprint='{cls.meta.blueprint_path}' "
            f"type={'Constant' if cls.meta.is_constant else 'Object'}>")


    # --- Definice __str__ pro definiční třídy ---#
    def __str__(cls) -> str:
        """
        Uživatelská reprezentace třídy.
        Vrací čisté byznysové jméno třídy.
        """
        return cls.__name__


    #--- Property usnadňující přístup k metadatům ---#
    @property
    def meta(cls) -> SimpleMetaType:
        """Veřejné rozhraní pro přístup k metadatům třídy."""
        # noinspection PyUnresolvedReferences
        return cls.__metadata__
