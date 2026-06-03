from datetime import datetime, date
from pathlib import Path
from enum import Enum


# serialization/Deserialize.py
class DeserializeValueMixin:
    """Deserializace hodnot ze slovníku na správné typy."""
    __slots__ = ()

    @classmethod
    def _deserialize_value(cls, key, value):
        """Převod hodnoty ze slovníku na správný typ podle metadat."""
        # Najdi inner podle name_snake
        if not cls.meta.inners:
            raise TypeError(f"Class {cls.__name__} has no inners to deserialize")

        inner = next((i for i in cls.meta.inners if i.name_snake == key), None)
        if not inner:
            raise TypeError(f"Unknown field '{key}' for {cls.__name__}")

        target_type = inner.meta.value_type

        # Primitivní typy
        if target_type in (str, int, float, bool):
            return target_type(value)

        # Datetime
        if target_type is datetime:
            return datetime.fromisoformat(value)

        # Date
        if target_type is date:
            return date.fromisoformat(value)

        # Path
        if target_type is Path:
            return Path(value)

        # Enum
        if isinstance(target_type, type) and issubclass(target_type, Enum):
            return target_type(value)

        # Explicitní kontrakt
        if hasattr(target_type, "from_dict") and callable(target_type.from_dict):
            return target_type.from_dict(value)

        # Neošetřený typ
        raise TypeError(
            f"Cannot deserialize field '{key}' of type {target_type}. "
            "Override _deserialize_value() to support this type."
        )

"""
2) Analýza DeserializeValueMixinTady začíná jít do tuhého, protože deserializace je "hádání" typů z plochých dat.Kritické postřehy:Vyhledávání v inners: next((i for i in cls.meta.inners if i.name_snake == key), None) – Tato operace proběhne pro každý klíč. Pokud máš objekt s 50 poli, je to $O(n^2)$ operace.Optimalizace: Měl bys využít cls.meta.param_map, což je dictionary, kde klíčem je právě name_snake. To je okamžitý přístup $O(1)$.Pevné typy vs. Flexibilita: Aktuálně deserializuješ pomocí target_type(value). To funguje pro int("10"), ale co když je target_type komplexní třída, která v __init__ vyžaduje víc argumentů?Řešení: Tvůj systém by se měl primárně spoléhat na to, že zavolá inner.class.from_dict(value) nebo prostě inner.class(value).Validace v deserializaci: Deserializace by neměla jen "přetypovat", ale rovnou i "validovat". Pokud int(value) selže, vyhodí to ValueError. Bylo by fajn to zabalit do tvé budoucí SimpleException.Drobná chyba v logice:Pythonif target_type in (str, int, float, bool):
    return target_type(value)
Pokud je target_type bool a ve value je string "False", tak bool("False") v Pythonu vrátí True (protože neprázdný string je True). Deserializace booleanů je v Pythonu zrádná a obvykle vyžaduje mapování "true"/"false", 1/0.
"""