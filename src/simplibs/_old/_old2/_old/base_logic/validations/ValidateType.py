from typing import Any, TYPE_CHECKING
# Outers
from ....utils import SimpleObjectLogicError

if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata


class ValidateType:
    """
    Mixin pro striktní runtime kontrolu datového typu hodnoty.
    """

    # Atribut 'meta' bude dostupný díky SimpleObjectMeta
    meta: 'SimpleObjectMetadata'

    @classmethod
    def validate_type(cls, value: Any, *, return_bool: bool = False) -> bool:
        """
        Provede deterministickou validaci typu na základě metadat třídy.

        Pokud hodnota neodpovídá 'value_type' definovanému v metadatech,
        buď vrátí False (pokud return_bool=True), nebo vyvolá výjimku.
        """

        # 1. Kontrola shody typu pomocí metadat (již dříve validovaných)
        if not isinstance(value, cls.meta.value_type):
            if return_bool:
                return False

            # Příprava srozumitelného popisu očekávaného typu
            if isinstance(cls.meta.value_type, tuple):
                expected_types = ", ".join(t.__name__ for t in cls.meta.value_type)
            else:
                expected_types = cls.meta.value_type.__name__

            # 2. Vyvolání logické výjimky s detailním kontextem
            raise SimpleObjectLogicError(
                error_name="TYPE ERROR",
                value_label="value",
                value=value,
                expected=f"Instance typu '{expected_types}'",
                problem=f"Předaná hodnota neodpovídá vyžadovanému typu pro třídu '{cls.__name__}'.",
                how_to_fix=(
                    f"Ujistěte se, že předávaná hodnota je instancí: {expected_types}.",
                    "Zkontrolujte, zda nedochází k nechtěné konverzi typu před touto validací."
                ),
                context=f"Runtime vynucení typu pro {cls.__name__}",
                exception=TypeError
            )

        return True


_DESIGN_NOTES = """
# ValidateType

## Účel
Tento mixin realizuje první úroveň ochrany dat v SimpleObjectu. Využívá 
deterministickou jistotu o typu, kterou jsme si připravili v metadatech.

## Logika
- **Striktnost**: Využívá `isinstance`, což je v Pythonu nejrychlejší a 
  nejspolehlivější cesta kontroly typu.
- **Flexibilita**: Díky `return_bool` může být tato metoda využita jak 
  v konstruktorech (kde chceme výjimku), tak v testovacích skriptech nebo 
  predikátech (kde chceme boolean).

## Propojení s Metadaty
Mixin přímo přistupuje k `cls.meta.value_type`. Tato vazba je bezpečná, 
protože metatřída garantuje existenci metadat dříve, než je jakákoliv 
runtime metoda zavolána.
"""