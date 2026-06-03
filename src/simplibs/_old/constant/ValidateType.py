from typing import Any, NoReturn
# Outers
from ....._types import MetaType
# Inners
from .exceptions.raise_type_error import raise_type_error


class ValidateType:
    """
    Mixin pro striktní runtime kontrolu datového typu hodnoty.
    """

    # Definice používaných prvků
    meta: MetaType

    @classmethod
    def validate_type(
        cls,
        value: Any,
        *,
        return_bool: bool = False
    ) -> bool | NoReturn:
        """
        Provede deterministickou validaci typu na základě metadat třídy.
        """

        # 1. Validace Happy path
        if isinstance(value, cls.meta.value_type):
            return True

        # 2. Vrácení bool negace
        if return_bool:
            return False

        # 3. Vyvolání výjimky
        raise_type_error(cls, value, cls.meta.value_type)




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