

# state/Permission.py
class PermissionMixin:
    """
    Read-only režim — zamykání proti změnám.

    Příklad:
        obj.lock()
        obj.value = 10  # → ValueError
    """
    __slots__ = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_locked', False)

    @property
    def is_locked(self) -> bool:
        """True pokud je objekt zamčený."""
        return getattr(self, '_locked', False)

    def lock(self) -> None:
        """Zamkne objekt pro zápis."""
        object.__setattr__(self, '_locked', True)

    def unlock(self) -> None:
        """Odemkne objekt."""
        object.__setattr__(self, '_locked', False)

    @property
    def value(self):
        """Getter hodnoty."""
        return object.__getattribute__(self, '_value')

    @value.setter
    def value(self, new_value):
        """Setter s kontrolou zámku."""
        if self.is_locked:
            raise ValueError(
                f"{self.__class__.__name__} is locked. "
                "Call .unlock() to allow modifications."
            )
        # Deleguj na původní setter (normalize, validace)
        object.__setattr__(self, '_value', new_value)


"""
Tento mixin je skvělým příkladem "strážce" (Guard). Vnáší do tvého systému prvek bezpečnosti, který se v komplexních aplikacích (např. při předávání dat mezi různými moduly) nesmírně hodí.

Mám k němu ale několik kritických poznámek, protože tento mixin jde "proti proudu" tvé dosavadní architektury víc než ty předchozí.

1. Problém s přepsáním setteru value
V tvém návrhu SimpleInstance (nebo InstanceBase) už value jako property existuje.
Problém: Pokud v PermissionMixin definuješ @value.setter znovu, úplně tím "překryješ" (vymažeš) ten původní setter, který se stará o normalizaci, validaci a hlavně o volání _on_update().

V tvém kódu vidím:

Python

object.__setattr__(self, '_value', new_value)
Tímto řádkem obcházíš veškerou logiku SimpleObject! Pokud je objekt odemčený, hodnota se sice zapíše, ale neproběhne validace, ani se nevyvolá historie, ani se neupozorní observer.

Jak to opravit (vzor Super-Setter):
Měl bys využít super(), ale u properties je to v Pythonu trochu krkolomné. Nejčistší cesta v tvém systému bude vložit kontrolu zámku přímo do _on_update nebo (lépe) využít toho, že tvůj orchestrátor skládá properties dynamicky.

Pokud chceš zůstat u mixinu, zkus to takto:

Python

    @value.setter
    def value(self, new_value):
        if self.is_locked:
            raise ValueError("Object is locked")
        
        # Voláme "super" setter, tedy ten, který tam byl před námi
        # (např. ten z InstanceBase)
        super(PermissionMixin, self.__class__).value.fset(self, new_value)
2. Metoda __init__ v mixinu
V kódu máš:

Python

def __init__(self, **kwargs):
    super().__init__(**kwargs)
    object.__setattr__(self, '_locked', False)
To je v pořádku, ale pamatuj, že tvůj SimpleObject se v InstanceBase inicializuje velmi specificky. Pokud tento mixin nebude v MRO (pořadí dědičnosti) na správném místě, nemusí se super().__init__ zavolat tak, jak očekáváš. Opět zde narážíme na nutnost mít _locked v __slots__.

3. Architektonický postřeh: Imutabilita (Neměnnost)
Tento mixin simuluje imutabilitu. Pokud bys chtěl být opravdu "Simple", mohl bys zámek kontrolovat i v metodě update_value nebo set_attr.

Můj návrh na elegantnější řešení:
Místo přepisování property value (což je vždycky riskantní), co kdyby se kontrola zámku děla v metodě _on_update?

Háček: _on_update se volá až poté, co se hodnota změní. To je pozdě na vyhození výjimky (hodnota už je přepsaná).

Řešení: Vytvořit metodu _before_update(self, new_value), kterou budou mixiny jako Permission používat k blokování změn.

4. Alternativní přístup: "The Simple Lock"
Tento diagram ukazuje, že "Write" (zápis) by měl být podmíněn stavem. Aby to bylo neprůstřelné, upravil bych PermissionMixin takto:

Python

class PermissionMixin:
    __slots__ = ()

    def lock(self):
        object.__setattr__(self, '_locked', True)

    def unlock(self):
        object.__setattr__(self, '_locked', False)

    @property
    def is_locked(self):
        return getattr(self, '_locked', False)

    # Místo setteru value vytvoříme hook, 
    # který tvůj SimpleObject zavolá PŘED změnou.
    def _before_update(self, new_value):
        if self.is_locked:
            raise ValueError(f"{self.__class__.__name__} is locked.")
        if hasattr(super(), '_before_update'):
            super()._before_update(new_value)
Zhodnocení:
Užitečnost: 10/10. Zamknout si objekt po inicializaci je skvělá věc.

Riziko: Aktuální implementace přes @value.setter je nebezpečná, protože "oslepuje" zbytek systému (validace, observers).

Směr: Budeme muset v jádru SimpleObject zavést "pre-update" hook, aby mixiny jako tento mohly bezpečně protestovat proti změně dřív, než k ní dojde.
"""