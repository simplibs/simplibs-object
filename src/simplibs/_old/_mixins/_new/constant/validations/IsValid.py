from typing import Any, Callable


class IsValid:
    """
    Mixin poskytující zjednodušené rozhraní pro ověření validity hodnoty.

    Slouží jako čitelná alternativa k metodě 'validate', pokud nás
    zajímá pouze logický výsledek (True/False).
    """

    # Definice používaných prvků
    validate: Callable

    @classmethod
    def is_valid(
        cls,
        value: Any
    ) -> bool:
        """
        Vrátí True, pokud hodnota projde kompletní validací, jinak False.

        Tato metoda nikdy nevyvolává výjimku, je určena pro použití
        v podmínkách (if) a filtrech.
        """

        # 1. Voláme hlavní validaci s vynuceným návratem booleanu
        return cls.validate(value, return_bool=True)


_DESIGN_NOTES = """
# IsValid

## Účel
Poskytuje čisté a intuitivní API pro situace, kdy vývojář nepotřebuje znát 
důvod selhání (výjimku), ale pouze potřebuje vědět, zda je hodnota 
přípustná pro danou třídu.

## Logika
- **Zapouzdření**: Jedná se o čistý wrapper nad `cls.validate(value, return_bool=True)`.
- **Čitelnost**: V kódu vypadá `if Age.is_valid(val):` mnohem lépe a srozumitelněji 
  než volání `validate` s parametry.
- **Bezpečnost**: Díky implementaci v `Validate.validate` máme jistotu, že i kdyby 
  uživatelská validace selhala na vnitřní chybě, `is_valid` bezpečně vrátí `False`.

## Použití
Ideální pro:
- Validaci vstupů ve webových formulářích.
- Filtrování kolekcí dat.
- Rychlé sanity checky před dalším zpracováním.
"""