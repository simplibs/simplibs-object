from typing import Any, Dict
from ..core.Metadata import MetadataMixin
from .Serialize import SerializeValueMixin
from .Deserialize import DeserializeValueMixin

# serialization/DictSerializer.py
class DictSerializerMixin(MetadataMixin, SerializeValueMixin, DeserializeValueMixin):
    """Převod objektu na/z dict."""
    __slots__ = ()

    def to_dict(self, _seen=None) -> Dict[str, Any]:
        """Exportuje objekt do slovníku."""
        if _seen is None:
            _seen = set()

        val = self._serialize_value(self.value, _seen=_seen)
        result = {self.meta.name_snake: val}

        if self.meta.inners:
            for inner_obj in self.meta.inners:
                inner_instance = getattr(self, inner_obj.name_snake)
                result.update(inner_instance.to_dict(_seen=_seen))

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Vytvoří instanci ze slovníku."""
        processed = {
            key: cls._deserialize_value(key, val)
            for key, val in data.items()
        }
        return cls(**processed)

"""
1) Analýza DictSerializerMixin
Tento mixin je "mozkem" transformace mezi objektem a čistým Python slovníkem.

Pozitiva:

Rekurzivní síla: Implementace to_dict správně kombinuje serializaci vlastní hodnoty a následnou iteraci přes inners.

Využití deserializace: from_dict elegantně využívá dříve definovanou _deserialize_value.

Kritické postřehy k logice to_dict:
Tady vidím jeden architektonický zádrhel. Tvůj kód dělá toto:

Python

result = {self.meta.name_snake: val}
if self.meta.inners:
    for inner_obj in self.meta.inners:
        result.update(inner_instance.to_dict(...))
Problém ploché struktury: Pokud máš objekt Auto a v něm inner Motor, tvoje to_dict vytvoří slovník, kde jsou obě věci na stejné úrovni (sourozenci), místo aby byl motor uvnitř auta. result.update totiž přepíše nebo přidá klíče do stejného slovníku.

Konvence: Většina serializátorů (jako Pydantic nebo Marshmallow) očekává, že to_dict vrátí data tak, jak jsou definována v atributech.

Doporučení: Pokud chceš zachovat hierarchii, měl by result vypadat spíše jako mapa jmen inner prvků na jejich hodnoty.

Kritické postřehy k from_dict:
Aktuálně děláš cls(**processed). To je super, pokud tvůj __init__ (nebo create_value) přijímá přesně tyto klíče. Jen pozor na to, že data ve from_dict může obsahovat i klíče, které v meta.inners nejsou – tvoje _deserialize_value tam sice má kontrolu, ale je dobré na to myslet.
"""


"""
Jak to propojit (Důležité pro zítřek)
Tyto dva mixiny jsou funkční nástroje, ale nejsou to konečné metody. Konečná metoda bude to_dict() a from_dict().

Můj návrh na strukturu Serialize.py (vysokoúrovňový):

Python

class SerializeMixin(SerializeValueMixin):
    def to_dict(self, _seen=None) -> dict:
        """Konečná metoda pro uživatele."""
        res = {}
        for inner in self.meta.inners:
            val = getattr(self, inner.name_snake).value
            res[inner.name_snake] = self._serialize_value(val, _seen=_seen)
        return res
Můj návrh na strukturu Deserialize.py (vysokoúrovňový):

Python

class DeserializeMixin(DeserializeValueMixin):
    @classmethod
    def from_dict(cls, data: dict) -> 'cls':
        """Vytvoří instanci třídy ze slovníku."""
        clean_data = {}
        for k, v in data.items():
            clean_data[k] = cls._deserialize_value(k, v)
        return cls(**clean_data)
"""