

# core/Metadata.py
class MetadataMixin:
    """Poskytuje instanci přímý přístup k metadatům."""
    __slots__ = ()

    @property
    def meta(self):
        """Zkratka pro přístup k metadatům."""
        # return self.__metadata__
        # self.__class__.__metadata__ je jistota, že saháme na metadata třídy
        # Proč použít self.__class__.__metadata__?
        # Protože metadata jsou v tvém návrhu sdílená pro všechny instance dané třídy
        # (jsou to data o struktuře, ne o konkrétních hodnotách).
        # Tímto zápisem dáváš jasně najevo, že instance nese odkaz
        # na "rodný list" své třídy.
        return self.__class__.__metadata__

    @property
    def name_readable(self) -> str:
        """Lidsky čitelné jméno objektu."""
        return self.meta.name_readable

    @property
    def name_snake(self) -> str:
        """Snake_case jméno objektu."""
        return self.meta.name_snake

    @property
    def value_type(self) -> type:
        """Typ hodnoty kterou objekt uchovává."""
        return self.meta.value_type

    @property
    def is_composite(self) -> bool:
        """True pokud má objekt vnitřní prvky (inners)."""
        return bool(self.meta.inners)

    @property
    def is_atom(self) -> bool:
        """True pokud objekt nemá vnitřní prvky."""
        return not bool(self.meta.inners)

    @property
    def DEFAULT(self):
        """Výchozí hodnota objektu."""
        return self.meta.default



    # Možná přidat i tyto:
    @property
    def param_names(self) -> list[str]:
        """Seznam jmen parametrů, ze kterých se objekt skládá."""
        return self.meta.param_names

    @property
    def owner(self) -> type:
        """Odkaz na původní třídu definice."""
        return self.meta.owner_class