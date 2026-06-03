from ._metadata import SimpleMeta
from ._types import SimpleMetaType


class SimpleBase(
    metaclass=SimpleMeta
):
    """
    Abstraktní kořenová třída pro všechny prvky systému Simple.

    Tato třída definuje společnou identitu pro konstanty i kompozitní objekty.
    Zajišťuje napojení na metatřídu a poskytuje jednotné rozhraní pro 
    přístup k metadatům.
    """

    # 1. Slot pro metadata - anotujeme základní strukturou metadat
    # Poznámka: Hodnota je dosazena metatřídou SimpleMeta při definici třídy
    __metadata__: SimpleMetaType

    # 2. Definice __slots__ pro samotnou bázi (pro výkon)
    __slots__ = ()

    # 3. Atribut potlačujícíinstanci pro základní třídy
    __allow_instantiation__ = False

    def __init__(self, *args, **kwargs):
        """
        Zákaz přímé inicializace základní třídy.
        SimpleBase slouží výhradně jako stavební prvek a typový identifikátor.
        """
        if not getattr(self, "__allow_instantiation__", False):
            raise TypeError(
                f"Třída {self.__class__.__name__} je abstraktní základ "
                "a nelze ji přímo instanciovat."
            )
        super().__init__(*args, **kwargs)

    @property
    def meta(self) -> SimpleMetaType:
        """
        Veřejný přístup k metadatům třídy. 
        metadata jsou uložena ve slotech pro maximální výkon a ochranu.
        """
        return self.__class__.__metadata__

    def __repr__(self) -> str:
        """
        Technická reprezentace objektu.
        Příklad: <AutoInstance target='Auto'>
        """
        return f"<{self.__class__.__name__} target='{self.meta.name_title}'>"

    def __str__(self) -> str:
        """
        Uživatelská reprezentace.
        Příklad: Auto
        """
        return self.meta.name_title


_DESING_NOTES = """
### Proč SimpleBase existuje?

* **Sjednocení pod jednu Metatřídu:**
    `SimpleMeta` je mozkem operace. Tím, že ji definujeme zde, garantujeme, že každý potomek (ať už `SimpleConstant` nebo `SimpleObject`) projde stejným procesem registrace a validace metadat, aniž by musel uživatel metatřídu ručně uvádět.
* **Typová Identita (Marker Interface):**
    V rámci celého frameworku nyní můžeme používat `isinstance(obj, SimpleBase)`. To nám dovoluje psát univerzální kód pro serializaci nebo validaci, který ví, že každý takový objekt má atribut `.meta`.
* **Ochrana integrity:**
    Zákaz přímé inicializace v `__init__` jasně deklaruje, že `SimpleBase` není "věc", ale "koncept". Skutečné věci jsou až konstanty a objekty.
* **Metadata Gateway:**
    Property `.meta` je jediným oficiálním oknem do vnitřního světa objektu. Tím, že je definována zde, je toto rozhraní pro všechny prvky systému symetrické.

---

### Role v mapě systému

`SimpleBase` funguje jako **přepínač mezi světem statického kódu a dynamických metadat**. Je to bod, kde končí běžná Python třída a začíná tvůj strukturovaný model reality.

"""