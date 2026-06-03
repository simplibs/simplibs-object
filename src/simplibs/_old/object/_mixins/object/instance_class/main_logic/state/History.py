from typing import Any, List, Tuple, Optional
from datetime import datetime


# state/History.py
class HistoryMixin:
    """
    Timeline tracking — ukládá změny s časovými razítky.

    Příklad:
        obj.value = 10
        obj.get_history()  # → [(datetime(...), 10), ...]
    """
    __slots__ = ()
    value: Any

    def _on_update(self) -> None:
        """Zaznamená změnu s timestampem."""
        super()._on_update()
        if not hasattr(self, '_timeline'):
            object.__setattr__(self, '_timeline', [])

        timeline = object.__getattribute__(self, '_timeline')
        timeline.append((datetime.now(), self.value))

    def get_history(self) -> List[Tuple[datetime, Any]]:
        """Vrátí seznam (timestamp, value) tuples."""
        return getattr(self, '_timeline', [])

    def get_value_at(self, timestamp: datetime) -> Optional[Any]:
        """Vrátí hodnotu platnou v daném čase (nejbližší předchozí)."""
        timeline = self.get_history()
        if not timeline:
            return None

        # Najdi poslední hodnotu před/v daném čase
        for ts, val in reversed(timeline):
            if ts <= timestamp:
                return val

        return None

"""
Tady už přituhuje! HistoryMixin je vynikající nástroj pro auditování dat nebo pro implementaci funkcí typu "Zpět" (Undo). Stejně jako u předchozích dynamických mixinů, i tady se ale potkávají tvé ambiciózní cíle (výkon přes __slots__) s praktickou implementací.

1. Konflikt s __slots__ a výkon
Opět narážíme na stejný problém jako u Event a Observable. Pokud _timeline nebude ve __slots__, volání object.__setattr__ selže.

Můj postřeh k výkonu:
U historie je riziko paměťové náročnosti nejvyšší. Pokud budeš mít 1000 objektů a každý změníš 100x, máš v paměti 100 000 záznamů.

Tip: Do budoucna by tento mixin mohl mít parametr (třeba v metadatech), který omezí délku historie (např. history_limit=10).

2. Časování a _on_update
V kódu máš:

Python

def _on_update(self) -> None:
    super()._on_update()
    # ... záznam do timeline ...
Tohle je v pořádku, ale je tu drobný háček. Záznam se vytvoří až po aktualizaci. To znamená, že historie obsahuje stav objektu po změně.

Co chybí? Pokud objekt vznikne (v __init__), jeho úplně první hodnota v historii není, protože _on_update se volá obvykle až při následných změnách (pokud ho nevoláš i v initu). Pro kompletní časovou osu by bylo dobré mít v historii i tu startovní hodnotu.

3. Logika v get_value_at
Metoda get_value_at je napsána lineárně (for ... in reversed). Pro krátkou historii je to naprosto v pohodě. Pokud by historie byla obrovská, v Pythonu by se pro efektivní hledání v seřazeném seznamu použil modul bisect. Ale pro tvé účely je tato verze čitelnější a bohatě stačí.

4. Návrh na "Simple" vylepšení
Aby byl mixin opravdu "profesionální", mohl by nabízet i jednoduchý rollback:

Python

    def undo(self) -> bool:
        """Vrátí objekt do předchozího stavu v historii. Vrací True při úspěchu."""
        timeline = self.get_history()
        if len(timeline) < 2:
            return False
            
        # Odstraň aktuální (poslední) záznam
        timeline.pop()
        # Získej ten před ním
        _, previous_value = timeline[-1]
        
        # Nastav hodnotu (to vyvolá nový záznam, takže pozor na zacyklení!)
        # Je lepší nastavit hodnotu přímo do jádra, aby se historie nezduplikovala
        self.value = previous_value 
        return True
Pozor na zacyklení: Pokud self.value = previous_value vyvolá _on_update, tak se nám do historie přidá záznam o tom, že jsme udělali undo. To je vlastně korektní (historie je lineární záznam času), ale je dobré s tím počítat.

5. Architektonické sjednocení
Už potřetí narážíme na potřebu "přidat slot" pro interní úložiště (_events, _observers_storage, _timeline).

Můj návrh:
Co kdybys v SimpleObjectMetadata nebo v továrně OBJECT udělal metodu, která projde všechny mixiny a podívá se, zda nemají definovaný speciální atribut, např. _REQUIRED_SLOTS = ('_timeline',)? Tím by se tvůj systém stal neprůstřelným a mohl bys používat čisté setattr/getattr.
"""