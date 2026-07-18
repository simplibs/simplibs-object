from typing import Set, Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .init_processors.names import create_names
from .init_processors.others import calculate_blueprint_path
from .validations import raise_metadata_is_immutable
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleBaseMetadataProtocol
    from ...protocols.classes import SimpleClassLike


class SimpleBaseMetadata:
    """
    Základní orchestrátor metadat systému Simple.
    Zajišťuje extrakci jmen a správu jmenného prostoru objektu.
    """

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = (
        # 1. Reference na třídu vlastníka
        "owner_class",

        # 2. Názvová identita (vypočtená z názvu třídy)
        "class_name",       # Např. "MojeData"
        "name_tuple",       # Např. ("Moje", "Data")
        "name_snake",       # Např. "moje_data"
        "name_private",     # Např. "_moje_data"

        # 3. Správa jmenného prostoru
        "node_names_set",       # Set použitých jmen pro detekci kolizí

        # 4. Pomocný předvýpočet pro __repr__
        "blueprint_path"
    )

    #--- Definice __init__ pro linicializaci hodnot ze slotů ---#
    # (přidává metodu skrze kterou se budou iniicalizovat potomci)
    def __init__(
        self: "SimpleBaseMetadataProtocol",
        owner_class: "SimpleClassLike"
    ) -> None:
        """
        Inicializuje základní metadata.
        Pokud je bypass=True, vytvoří pouze prázdnou schránku pro systémové báze.
        """
        # 1. Přiřazení třídy
        self.owner_class = owner_class

        # 2. Výpočet jmenné identity
        self.class_name = owner_class.__name__
        (self.name_tuple,
         self.name_snake,
         self.name_private) = create_names(owner_class)

        # 3. Registrace jména do setu použitých jmen (základ pro budoucí validace inners)
        self.node_names_set: Set[str] = {self.name_snake}

        # 4. Příprava parametru pro vytváření repr
        self.blueprint_path = calculate_blueprint_path(owner_class)

        # 5. Spuštění metod pro integraci logiky potomků
        self._process_user_data()

    #--- Definice metody pro inicializaci potomků ---#
    # (potomci nemají vlastní init a používají tuto metodu)
    def _process_user_data(
        self: "SimpleBaseMetadataProtocol"
    ) -> None:
        """
        Hook pro procesy specifické pro daný typ metadata.

        Výchozí implementace: žádný obsah.
        Určeno pro přepsání v podtřídách.
        """
        pass

    #--- Metoda pro zápis atributů metadatové třídy ---#
    # (zamezuje přepisu již zadaných dat)
    def __setattr__(
        self: "SimpleBaseMetadataProtocol",
        attr_name: str,
        new_value: Any
    ) -> None:
        """Povolí zápis pouze pokud je pole UNSET nebo patří do cache."""

        # 1. Získání aktuální hodnoty
        current_value = getattr(self, attr_name, UNSET)

        # 2. Kontrola zda přepisujeme jen nedefinovaný prvek
        if current_value is not UNSET:
            raise_metadata_is_immutable(attr_name, current_value, new_value, self.owner_class)

        # 3. Provedení zápisu
        super().__setattr__(attr_name, new_value)