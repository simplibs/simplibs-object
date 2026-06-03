from typing import Any
from simplibs.signature import create_keyword_parameter
from simplibs.sentinels import EMPTY
# Inners
from ._SimpleBaseMetadata import SimpleBaseMetadata
from .processors.attributes import process_type, process_default_for_constant
from .processors.methods import process_classmethod
from .utils.class_builders import make_core_class, make_atom_class
from .utils.param_builders import make_atom_param


# noinspection PyAttributeOutsideInit
class SimpleConstantMetadata(SimpleBaseMetadata):
    """
    Specializovaný orchestrátor pro konstanty (Atomy).
    Zajišťuje, že každý list systému má jasně definovaný typ,
    validní výchozí hodnotu a funkční validační rozhraní.
    """

    __slots__ = (
        # Typová a hodnotová integrita
        "value_type",  # Normalizovaný typ (_type)
        "default",  # Výchozí hodnota (_default)
        "validate",  # Reference na metodu _validate

        # Veřejné rozhraní (Signatura)
        "is_user_code",
        "is_constant",

        # Cache pro dynamické objekty
        "_atom_param",
        "_core_class",
        "_atom_class",
    )

    def _process_user_interface(self):

        # 1. Definice bool parametrů
        self.is_constant = True
        self.is_user_code = True

        # 2. Zpracování _type
        self.value_type = process_type(
            owner_class=self.owner_class
        )

        # 3. Zpracování _default
        self.default = process_default_for_constant(
            default_type=self.value_type,
            owner_class=self.owner_class
        )

        # 4. Zpracování _validate
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

    def _prepare_cache_attributes(self):
        """Inicializace cache slotů do výchozího stavu."""
        self._atom_param = EMPTY
        self._core_class = EMPTY
        self._atom_class = EMPTY

    @property
    def atom_param(self):
        """Lazy brána k signatuře parametru."""
        if self._atom_param is EMPTY:
            self._atom_param = make_atom_param(self.owner_class)
        return self._atom_param

    @property
    def core_class(self):
        """Lazy brána k core instanci parametru."""
        if self._core_class is EMPTY:
            self._core_class = make_core_class(self.owner_class)
        return self._core_class

    @property
    def atom_class(self):
        """Lazy brána k atomické instanci parametru."""
        if self._atom_class is EMPTY:
            self._atom_class = make_atom_class(self.owner_class)
        return self._atom_class




_DESIGN_NOTES = """
## Účel
Tento orchestrátor transformuje statickou definici konstanty na aktivní datový prvek. Jeho hlavním úkolem je garantovat, že **výchozí stav je vždy legální**. Pokud konstanta projde tímto procesem, framework má jistotu, že její `_default` odpovídá `_type` a projde i svou vlastní metodou `_validate`.

## Logika / Tok zpracování
1.  **Dědičnost Identity:** Prvním krokem je vždy volání `super().__init__`, čímž objekt získá své "jméno a občanství" v systému skrze `SimpleBaseMetadata`.
2.  **Typová kotva:** Normalizuje `_type`. To je kritické pro následnou validaci `isinstance`, aby si systém poradil i s Uniony nebo složitějšími zápisy typů.
3.  **Cross-Validation:** Provádí křížovou kontrolu mezi třemi body: Hodnotou, Typem a Validační metodou. Tento trojúhelník tvoří "neprůstřelnou" definici konstanty.
4.  **Signature Crystallization:** Vytváří `atom_param`. Tato signatura je "vyslanec" konstanty, kterého si později přebírá `SimpleObjectMetadata`, aby z něj postavil parametry pro `_logic`.

## Poznámky
- **Nulová tolerance:** Pokud `_default` nevyhovuje `_validate`, proces se zastaví okamžitě při importu. Tím se předchází chybám, které by se jinak projevily až hluboko v runtime.
- **Lehkost:** Na rozdíl od kompozic tento orchestrátor neřeší grafy ani dekompozici, což z něj dělá velmi rychlou komponentu pro základní stavební kameny.
- **Příprava na Runtime:** Sloty `core_class` a `instance_class` jsou připraveny pro uložení dynamicky vygenerovaných tříd, které budou obstarávat samotnou práci s hodnotami.

"""