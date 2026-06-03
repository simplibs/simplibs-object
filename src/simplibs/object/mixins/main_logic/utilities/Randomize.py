from typing import Any
from datetime import datetime, date, timedelta
from pathlib import Path
from enum import Enum
import random
import string

from ..core.Metadata import MetadataMixin


# utilities/Randomize.py
class RandomizeMixin(MetadataMixin):
    """
    Generování náhodných dat podle typu — užitečné pro testy.

    Příklad:
        obj.fill_random()  # naplní náhodnými daty
    """
    __slots__ = ()

    def fill_random(self) -> None:
        """Naplní objekt náhodnými daty podle value_type."""
        if self.meta.inners:
            # Rekurzivně naplň všechny inners
            for inner in self.meta.inners:
                inner_instance = getattr(self, inner.name_snake)
                if hasattr(inner_instance, 'fill_random'):
                    inner_instance.fill_random()
        else:
            # Generuj podle typu
            self.value = self._generate_random_value(self.meta.value_type)

    def _generate_random_value(self, target_type: type) -> Any:
        """Vygeneruje náhodnou hodnotu podle typu."""
        # Primitivní typy
        if target_type is int or target_type == int:
            return random.randint(0, 1000)

        if target_type is float or target_type == float:
            return round(random.uniform(0, 1000), 2)

        if target_type is str or target_type == str:
            length = random.randint(5, 15)
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        if target_type is bool or target_type == bool:
            return random.choice([True, False])

        # Datetime
        if target_type is datetime or target_type == datetime:
            start = datetime(2020, 1, 1)
            end = datetime(2025, 12, 31)
            delta = end - start
            random_days = random.randint(0, delta.days)
            return start + timedelta(days=random_days)

        # Date
        if target_type is date or target_type == date:
            start = date(2020, 1, 1)
            end = date(2025, 12, 31)
            delta = end - start
            random_days = random.randint(0, delta.days)
            return start + timedelta(days=random_days)

        # Path
        if target_type is Path or target_type == Path:
            random_name = ''.join(random.choices(string.ascii_lowercase, k=10))
            return Path(f"/tmp/{random_name}.txt")

        # List
        if hasattr(target_type, '__origin__') and target_type.__origin__ is list:
            # typing.List[int] apod.
            length = random.randint(3, 10)
            item_type = target_type.__args__[0] if target_type.__args__ else int
            return [self._generate_random_value(item_type) for _ in range(length)]

        # Dict
        if hasattr(target_type, '__origin__') and target_type.__origin__ is dict:
            length = random.randint(2, 5)
            key_type = target_type.__args__[0] if len(target_type.__args__) > 0 else str
            val_type = target_type.__args__[1] if len(target_type.__args__) > 1 else int
            return {
                self._generate_random_value(key_type): self._generate_random_value(val_type)
                for _ in range(length)
            }

        # Enum
        if isinstance(target_type, type) and issubclass(target_type, Enum):
            return random.choice(list(target_type))

        # Fallback — None nebo prázdný string
        return None if random.choice([True, False]) else ""


"""
Tento mixin je naprosto geniální pro prototypování a automatizované testování. Vytvořit si celou složitou strukturu objektů a jedním zavoláním fill_random() ji oživit daty, je přesně ten typ "developer experience" (DX), o který nám jde.

Pojďme nejdříve k tvé úvaze o rozdělení a pak k samotnému kódu.

Rozdělení na atomy vs. univerzální metoda
Tvůj pocit, že by to uživatel mohl chtít "osekat", je správný, ale v tomto případě bych se držel univerzální implementace z těchto důvodů:

Sémantická celistvost: fill_random je jedna akce. Kdybys to rozdělil na RandomIntMixin, RandomStrMixin atd., musel by uživatel při definici třídy přesně vědět, jaké typy bude používat, a namíchat si jich třeba deset. To popírá princip "Simple".

Lepší cesta (Override): Pokud uživatel chce generovat data jinak (např. jména z reálného seznamu místo náhodných písmen), nejlepší cesta v OOP je prostě metodu _generate_random_value ve své třídě přepsat.

Registr generátorů: Pokud bys chtěl být hodně pokročilý, místo rozdělování mixinů bys mohl mít v rámci tohoto mixinu slovník (mapu) TYPE_GENERATORS, kam by si uživatel mohl zaregistrovat vlastní funkci pro specifický typ.

Závěr: Nech to jako jeden mixin, ale udělej ho maximálně rozšiřitelný skrze vnitřní metody.

Analýza kódu RandomizeMixin
1. Rekurze a Inners
Python

inner_instance = getattr(self, inner.name_snake)
if hasattr(inner_instance, 'fill_random'):
    inner_instance.fill_random()
Tady je opět ta naše klasická otázka: Je inner_instance už SimpleObject (s mixiny), nebo jen Atom? Pokud je to jen Atom, fill_random mít nebude a nic se nestane. To je v pořádku, ale znamená to, že pokud chceme hloubkové plnění, musí mít i vnitřní prvky tento mixin.

2. Typová kontrola (typing.List, typing.Dict)
Použití __origin__ a __args__ pro detekci vnitřků seznamů a slovníků je profesionální přístup. Tím tvá knihovna získává body za moderní Python (Type Hints).

3. Logika Fallbacku
Python

return None if random.choice([True, False]) else ""
Tady bych byl opatrný. Pokud je target_type třeba moje vlastní třída, vrátit None nebo "" může rozbít validaci.

Tip: Pokud typ neznáš a není to tvoje Base třída, možná by bylo lepší vyhodit varování nebo se pokusit o target_type().

Kritické postřehy k logice
Respektování Validací: To je největší výzva. Tvůj generátor může vytvořit číslo 500, ale uživatel může mít v Validatoru nastaveno, že věk musí být 0-120.

Řešení: Po vygenerování hodnoty by se měla zkusit validace. Pokud neprojde, zkusit to znovu (třeba 3x) nebo hodit chybu.

Enumy:

Python

return random.choice(list(target_type))
Tohle je perfektní a velmi užitečné!

Architektonické doporučení pro zítřek
Až se zítra pustíme do "velkého propojování", navrhuji u tohoto mixinu toto:

Přidat podporu pro "Range" z metadat: Pokud v metadatech budeme mít (výhledově) informaci o min/max, tento mixin by ji měl brát v úvahu.

Metoda fill_random vs generate: Možná by bylo fajn mít i classmethodu create_random(), která rovnou vrátí novou instanci naplněnou daty (továrna na testovací data).
"""