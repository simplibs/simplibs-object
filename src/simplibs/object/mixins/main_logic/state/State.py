from typing import Any, List


# state/State.py
class StateMixin:
    """
    Sledování změn — dirty tracking, reset, historie.

    Příklad:
        obj.value = 10
        obj.is_dirty  # → True
        obj.reset()   # → zpět na původní hodnotu
    """
    __slots__ = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Uložíme počáteční stav
        object.__setattr__(self, '_initial_value', self.value)
        object.__setattr__(self, '_history', [self.value])

    @property
    def is_dirty(self) -> bool:
        """True pokud se aktuální hodnota liší od počáteční."""
        return self.value != self._initial_value

    def reset(self) -> None:
        """Vrátí hodnotu na původní úroveň."""
        self.value = self._initial_value

    @property
    def history(self) -> List[Any]:
        """Seznam všech hodnot které objekt měl."""
        return self._history

    def _on_update(self) -> None:
        """Zaznamená změnu do historie."""
        super()._on_update()
        if self.value != self._history[-1]:
            self._history.append(self.value)


"""
StateMixin je v podstatě "odlehčená" verze historie, kterou jsme probírali dříve, ale s velmi důležitým konceptem Dirty Trackingu. Ten je naprosto klíčový pro databázové operace (ukládáme jen to, co se skutečně změnilo).

1. Analýza logiky StateMixin
To dobré:

Dirty Tracking: Porovnání self.value != self._initial_value je jednoduché a efektivní.

Reset: Možnost vrátit objekt do původního stavu je pro uživatele velmi pohodlná (např. tlačítko "Zrušit změny" ve formuláři).

Optimalizace historie: Podmínka if self.value != self._history[-1] v _on_update je skvělá – zabraňuješ tím duplicitním záznamům v historii, pokud někdo nastaví stejnou hodnotu, která už v objektu je.

Na co si dát pozor:

Mutable objekty: Pokud je self.value například seznam (list) nebo slovník (dict), pak se změnou obsahu (např. obj.value.append(1)) změní i _initial_value, protože obě proměnné ukazují na stejný objekt v paměti. V tom případě by is_dirty vždy vracelo False.

Zítřejší úkol: V __init__ budeme muset u mutable typů dělat deepcopy.

Duplicita s HistoryMixin: Všimni si, že tento mixin si drží vlastní _history. Pokud uživatel použije HistoryMixin (ten s časy) i StateMixin, bude mít v paměti dvě verze historie.

Úvaha: Možná by stálo za to tyto dva mixiny sjednotit nebo je nechat dědit ze společného základu.

2. Architektonický postřeh: __init__ a __slots__
Tady opět narážíme na stejnou písničku:

Slots: _initial_value a _history musí být ve slotech.

Pořadí inicializace: V __init__ voláš self.value. To znamená, že v momentě inicializace tohoto mixinu už musí být value (nebo vnitřní Atom) vytvořena. To tvůj generátor tříd musí zajistit správným pořadím v MRO.
"""