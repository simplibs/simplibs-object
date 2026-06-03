from ..._types import SimpleMetaType, SimpleClassType


class InstanceBase:
    """Společný jmenovatel a garant identity pro všechny naše instance."""

    # 1. Definice třídního atribut zajištujícího že se nebudou počítat metadata
    # a ty tak budou přejmutá z deklarační třídy.
    _is_instance_class: bool = True

    # 2. Nastavení slotu a slabé reference pro podporu hashování
    __slots__ = ("__weakref__",)

    # 3. Definice pomocné metody pro mixiny skrze kterou mají přístup do initu třídy
    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        pass

    #--- Definice protperty zpřístupňující meta ---#
    # (pro přímí přístup bez procházení MRO)
    @property
    def meta(self: SimpleClassType) -> SimpleMetaType:
        """
        Veřejný přístup k metadatům třídy.
        metadata jsou uložena ve slotech pro maximální výkon a ochranu.
        """
        return self.__class__.__metadata__

    #--- Definice __repr__ (reprezentačního řetězce objektu) ---#
    # (univerzální definice společná všem potomkům)
    def __repr__(self) -> str:
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

    #--- Definice __str__ (řetězec reprezentující jméno třídy) ---#
    # (univerzální definice společná všem potomkům)
    def __str__(self) -> str:
        """
        Uživatelská reprezentace.
        Příklad: Auto
        """
        return self.meta.class_name