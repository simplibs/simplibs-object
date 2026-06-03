from typing import Any

from ..core.Logic import LogicMixin
from ..core.Validate import ValidateMixin
from ..serialization.DictSerializer import DictSerializerMixin


# mutation/Mutation.py
class MutationMixin(LogicMixin, ValidateMixin, DictSerializerMixin):
    """Kompletní mixin pro mutace objektů — kopie, modifikace, výpočty."""
    __slots__ = ()

    def copy_self(self):
        """Vytvoří identickou kopii aktuálního objektu."""
        return self.from_dict(self.to_dict())

    def create_modified_instance(self, **kwargs):
        """
        Vytvoří kopii objektu s přepsanými parametry.

        Příklad:
            user.create_modified_instance(age=31)

        Validace probíhá automaticky přes __init__ → property setter → normalize().
        """
        current_data = self.to_dict()
        current_data.update(kwargs)
        return self.from_dict(current_data)

    def get_calculated_value(self, **kwargs) -> Any:
        """
        Vypočítá a vrátí hlavní hodnotu s novými parametry.
        Původní instance zůstává nezměněna.

        Příklad:
            new_total = price.get_calculated_value(tax=0.21)
        """
        temporary_instance = self.create_modified_instance(**kwargs)
        return temporary_instance.value

    def apply_update(self, **kwargs) -> Any:
        """
        Mutuje self.value na místě pomocou update_value().

        Příklad:
            obj.apply_update(width=100, height=200)

        Spustí _on_update() hook.
        """
        new_value = self.update_value(value=self.value, **kwargs)
        self.value = new_value
        if hasattr(self, "_on_update") and callable(self._on_update):
            self._on_update()
        return new_value


"""
1. Metoda copy_self a create_modified_instance
Tento přístup je geniální ve své jednoduchosti. Místo složitého řešení copy.deepcopy() využíváš již hotový a otestovaný "round-trip" přes slovník.

Výhoda: Máš 100% jistotu, že kopie projde znovu validací a normalizací. Pokud se změnila pravidla validace mezi vytvořením původního objektu a kopií, kopie na to upozorní.

Postřeh k create_modified_instance: Je to v podstatě tvůj vlastní replace() (jako mají namedtuples).

Tip: Pokud bys chtěl být extrémně efektivní, mohl by ses pokusit o "shallow copy", ale tvůj přístup přes to_dict a from_dict je neprůstřelný, protože čistí data od případných nechtěných referencí v paměti.

2. Metoda get_calculated_value
Tato metoda je velmi užitečná pro scénáře typu "Co když?".

Příklad: Máš objekt Sleva, která počítá výslednou cenu. Chceš vědět, kolik by to bylo, kdyby sleva byla 20 % místo 10 %, ale nechceš ten objekt měnit.

Logika: Vytvoření temporary_instance je čisté. Jen pozor na výkon – u obřích struktur může být vytváření celé instance jen kvůli jednomu výpočtu drahé. Ale pro standardní byznys logiku je to naprosto v pořádku a velmi bezpečné.

3. Metoda apply_update (In-place mutace)
Tady se dostáváme k zásadnímu momentu – změně stavu existujícího objektu.

Analýza: ```python
new_value = self.update_value(value=self.value, **kwargs)
self.value = new_value

Tento kód je správně, protože volá `update_value` z `LogicMixin`, který ví, jak zkombinovat starou hodnotu s novými parametry.
Duplicita událostí: Pozor na jednu věc. Pokud self.value = new_value (setter v InstanceBase) už sám o sobě volá self._on_update(), tak tvůj kód v apply_update jej zavolá podruhé.

Doporučení: Zítra v rámci sjednocení zajistíme, aby se _on_update() volal vždy jen jednou na konci celé operace.

Architektonické postřehy k celku
Klíčové dilema: Vnořená data v to_dict
Jak jsme narazili u serializace: aby copy_self a create_modified_instance fungovaly správně, musí být struktura slovníku z to_dict kompatibilní s tím, co očekává __init__.
Pokud to_dict vrací vnořené objekty jako slovníky, tvůj __init__ (nebo továrna) musí umět tyto slovníky zase přeměnit na objekty. To už máš víceméně vyřešeno v DeserializeValueMixin, takže to do sebe krásně zapadá.

Chybějící kousek: update_self vs create_modified
Máš metodu pro vytvoření nové modifikované instance a metodu pro mutaci hodnoty. Chybí ti metoda pro "Deep Update" na místě. Tedy něco jako:

Python

def update_from_dict(self, data: dict):
    """Aktualizuje vnitřní prvky (inners) z dodaného slovníku."""
    for key, val in data.items():
        if hasattr(self, key):
            # Zde by se využila tvoje logika pro set_attr
            setattr(self, key, val) 
Závěrečné shrnutí mutací
MutationMixin je v tuto chvíli vrcholem tvé pyramidy. Využívá všechny vrstvy pod sebou:

Logic pro výpočet nové hodnoty.

Validate pro kontrolu správnosti.

Serialization pro přenos dat.
"""