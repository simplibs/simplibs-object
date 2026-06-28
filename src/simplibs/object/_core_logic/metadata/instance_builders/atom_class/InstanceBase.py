from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import InstanceBaseProtocol


class InstanceBase:
    """Společný jmenovatel a garant identity pro všechny naše instance."""

    # 1. Nastavení slotu a slabé reference pro podporu hashování
    __slots__ = ("__weakref__",)

    # 2. Definice pomocné metody pro mixiny skrze kterou mají přístup do initu třídy
    def init_mixins(
        self: "InstanceBaseProtocol"
    ) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        pass

    # 3. Definice protperty zpřístupňující meta
    # (pro přímí přístup bez procházení MRO)
    @property
    def meta(
        self: "InstanceBaseProtocol"
    ) -> "SimpleMetadataLike":
        """
        Veřejný přístup k metadatům třídy.
        metadata jsou uložena ve slotech pro maximální výkon a ochranu.
        """
        return self.__class__.__metadata__

    # 4. Definice __repr__ (reprezentačního řetězce objektu)
    # (univerzální definice společná všem potomkům)
    def __repr__(
        self: "InstanceBaseProtocol"
    ) -> str:
        """
        Unifikovaná technická reprezentace pro všechny prvky systému Simple.
        Nenaznačuje možnost předávání parametrů do initu, ale transparentně
        ukazuje typ, původ, stav a paměťové ID.
        """
        class_name  = self.meta.class_name
        blueprint   = f"blueprint='{self.meta.blueprint_path}'"
        state       = f"value={self._value!r}" if hasattr(self, "_value") else ""
        hex_id      = f"id={hex(id(self))}"

        return f"<{class_name} {blueprint} {state} {hex_id}>"

    # 5. Definice __str__ (řetězec reprezentující jméno třídy)
    # (univerzální definice společná všem potomkům)
    def __str__(
        self: "InstanceBaseProtocol"
    ) -> str:
        """
        Uživatelská reprezentace.
        Příklad: Auto
        """
        return self.meta.class_name