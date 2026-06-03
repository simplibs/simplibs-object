from typing import Type, Any, Dict, Tuple
# Outers
from .._types import SimpleClassType, SimpleMetaType
# Inners
from ._SimpleBaseMetadata import SimpleBaseMetadata
from ._SimpleConstantMetadata import SimpleConstantMetadata
from ._SimpleObjectMetadata import SimpleObjectMetadata
from .utils import create_root_metadata
from .validations import raise_frozen_attribute_error

# Mapování systémových kořenů na jejich metadata třídy
_ROOT_METADATA_MAPPING = {
    "SimpleBase": SimpleBaseMetadata,
    "SimpleConstant": SimpleConstantMetadata,
    "SimpleObject": SimpleObjectMetadata,
}

# Zmrazené prvky definující rozhraní třídy
_FROZEN_ATTRS = frozenset({
    "_default", "_type", "_inners", "_logic", "_decompose", "_validate"
})


class SimpleMeta(type):
    """
    Metatřída systému Simple. Zajišťuje automatickou orchestraci metadat
    při definici třídy a chrání integritu jejího rozhraní.
    """

    def __setattr__(
        cls,
        attr_name: str,
        new_value: Any
    ) -> None:
        """Implementuje 'Frozen State' pro klíčové definiční atributy."""

        # 1. Kontrola zda nedochází k přepisu zmrazeného atributu
        if attr_name in _FROZEN_ATTRS:
            raise_frozen_attribute_error(cls, attr_name, new_value)

        # 2. Zápis hodnoty
        super().__setattr__(attr_name, new_value)

    def __new__(
        mcls: type | SimpleClassType,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> SimpleClassType:
        """
        Analyzuje vznikající třídu a rozhoduje o jejím zařazení (Kořen/Konstanta/Kompozice).
        """
        # 1. Vytvoření objektu třídy
        cls = super().__new__(mcls, name, bases, namespace)

        # 2. Zpracování metadat základních tříd
        if name in _ROOT_METADATA_MAPPING:
            metadata_cls = _ROOT_METADATA_MAPPING[name]
            cls.__metadata__ = create_root_metadata(metadata_cls, cls)

        # 3. Zpracování metadat kompozice (potomci SimpleObject)
        elif hasattr(cls, "_inners"):
            cls.__metadata__ = SimpleObjectMetadata(owner_class=cls)

        # 4. Zpracování metadat konstanty (potomci SimpleConstant)
        else:
            cls.__metadata__ = SimpleConstantMetadata(owner_class=cls)

        # 5. Navrácení zvalidované třídy
        return cls

    @property
    def meta(cls: SimpleClassType) -> SimpleMetaType:
        """Veřejné rozhraní pro přístup k metadatům třídy."""
        return cls.__metadata__


_DESIGN_NOTES = """
## Účel
SimpleMeta funguje jako "továrna na třídy", která automatizuje jejich zrod. Hlavním cílem je absolutní odstínění vývojáře od vnitřních procesů orchestrace. Metatřída rozpozná záměr (dědičnost z kořenů vs. definice obsahu) a zajistí, že každá třída má v momentě svého vzniku připravený validovaný metadatový kontext.

## Logika / Tok zpracování
1.  **Diferenciace kořenů:** Pomocí `_ROOT_NAMES` identifikuje základní kameny systému. Pro tyto třídy volá specializovanou metodu `create_empty`, která vytvoří "tichý" kontext bez spouštění validací, čímž zajišťuje stabilitu základů frameworku.
2.  **Strukturální Heuristika:** * Přítomnost `_inners` v namespace automaticky přepíná na `SimpleObjectMetadata`.
    * Absence `_inners` u tříd mimo kořeny automaticky aktivuje `SimpleConstantMetadata`.
3.  **Garantovaná Identita:** Každý vzniklý objekt třídy získá atribut `__metadata__`, který je díky dědičnosti orchestrátorů konzistentní v přístupu k názvům a identitě (`owner_class`).
4.  **Ochrana DNA:** Metoda `__setattr__` funguje jako zámek. Jakmile je třída definována, její klíčové parametry jsou zafixovány, což brání nechtěným vedlejším účinkům v runtime.

## Poznámky
- **Delegování zodpovědnosti:** Metatřída již neřeší, jak se "čistí sloty". Tato logika byla úspěšně delegována na orchestrátory, což snižuje riziko chyb při rozšiřování systému.
- **Prediktivní chování:** Díky jasnému rozdělení mezi Konstanty a Kompozice nedochází ke smíšeným stavům, což zjednodušuje následné generování signatur a logiky výpočtů.
- **Vysoká granularita:** Každá větev systému má přesně ty informace, které potřebuje (Konstanta typy, Kompozice strukturu), bez zbytečného informačního balastu.

"""