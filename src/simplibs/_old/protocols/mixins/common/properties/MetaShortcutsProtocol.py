from typing import Protocol, runtime_checkable, Any
# Outers
from ....types import SimpleInstanceType


@runtime_checkable
class MetaShortcutsProtocol(SimpleInstanceType, Protocol):
    """
    Protokol pro mixin MetaShortcuts.

    Garantuje přítomnost ergonomických zkratek (properties) přímo na instanci,
    které zprostředkovávají rychlý přístup k často dotazovaným metadatům třídy.
    """

    # --- IDENTITA OBJEKTU ---
    @property
    def name_snake(self) -> str:
        """Snake_case jméno třídy objektu (např. 'moje_data')."""
        ...

    # --- TYPOVÁ INFORMACE ---
    @property
    def value_type(self) -> type:
        """Originální Python typ hodnoty, kterou objekt reprezentuje."""
        ...

    @property
    def default(self) -> Any:
        """Výchozí (defaultní) hodnota objektu definovaná v jeho metadatech."""
        ...

    # --- STRUKTURA OBJEKTU ---
    @property
    def is_atom(self) -> bool:
        """Vrací True, pokud objekt představuje Atom (nemá žádné vnitřní prvky)."""
        ...

    @property
    def is_composite(self) -> bool:
        """Vrací True, pokud objekt představuje Kompozici (skládá se z vnitřních prvků)."""
        ...

    @property
    def is_decomposeable(self) -> bool:
        """Vrací True, pokud objekt podporuje logiku rozkladu (dekompozice) hlavní hodnoty."""
        ...