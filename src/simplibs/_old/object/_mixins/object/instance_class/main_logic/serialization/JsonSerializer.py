import json
from .DictSerializer import DictSerializerMixin

# serialization/JsonSerializer.py
class JsonSerializerMixin(DictSerializerMixin):
    """Převod objektu na/z JSON."""
    __slots__ = ()

    def to_json(self, **kwargs) -> str:
        """Převede objekt na JSON řetězec."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    @classmethod
    def from_json(cls, json_str: str):
        """Vytvoří instanci z JSON řetězce."""
        return cls.from_dict(json.loads(json_str))

"""
2) Analýza JsonSerializerMixin
Tento mixin je ukázkově minimalistický a přesně takový má být.

Pozitiva:

DRY (Don't Repeat Yourself): Správně dědí z DictSerializerMixin, takže neopakuješ logiku transformace, jen měníš formát (dict -> str).

Kódování: ensure_ascii=False je v roce 2026 naprostá nutnost pro správnou podporu češtiny a emojis.

Flexibilita: Předávání **kwargs do json.dumps je profi přístup. Uživatel si tak může snadno přidat indent=4 pro hezké formátování.

Doporučení:

Statické metody: U from_json by se dalo uvažovat o robustnějším ošetření chyb. Pokud přijde nevalidní JSON (třeba uříznutý string), json.loads vyhodí JSONDecodeError. Bylo by fajn to v budoucnu zabalit do SimpleSerializationError.
"""