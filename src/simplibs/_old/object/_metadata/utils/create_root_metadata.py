from typing import Type, Set, Any
from simplibs.sentinels import UNSET
# Outers
from ..._types import SimpleClassType


def create_root_metadata(
    metadata_cls: Type,
    owner_class: SimpleClassType
) -> Any:
    """
    Vytvoří inertní instanci metadat pro systémové kořeny.
    Obchází standardní inicializační proces, aby zabránila validaci
    neúplných dat u základních tříd frameworku.
    """

    # 1. Vytvoření instance bez volání __init__
    meta = object.__new__(metadata_cls)

    # 2. Sběr všech slotů v hierarchii
    all_slots: Set[str] = set()
    for c in type.mro(metadata_cls):
        if hasattr(c, '__slots__'):
            all_slots.update(c.__slots__)

    # 3. Inicializace VŠECH slotů na UNSET
    # Tím zajistíme, že i cache sloty jsou UNSET.
    # To je důležité: u ROOT třídy nechceme EMPTY (připraveno),
    # ale UNSET (zde se nic dít nebude).
    for slot in all_slots:
        object.__setattr__(meta, slot, UNSET)

    # 4. Nastavení základní identity
    meta.owner_class = owner_class

    # 5. Explicitní nastavení klíčových příznaků
    # U Root tříd jsou tyto věci irelevantní, ale pro jistotu:
    if "is_user_code" in all_slots:
        meta.is_user_code = False

    if "is_constant" in all_slots:
        meta.is_constant = False

    return meta


_DESING_NOTES = """
Proč mít 4. a 5. bod:

Tvoje úvaha je naprosto racionální. Jako programátoři se často rozhodujeme mezi **Pragmatismem** (nedělat věci, které nepotřebuji) a **Robustností** (připravit systém na vše).

U těchto dvou základních tříd (`SimpleObject` a `SimpleConstant`) je pravda, že v 99 % času budou jen "mrtvými" předlohami v kódu. Nicméně existují **3 reálné scénáře**, kdy se ti to, že i tyto třídy mají validní metadata (včetně `owner_class` a `is_user_code`), bude náramně hodit:

### 1. Průchod celou hierarchií (Introspekce)
Představ si, že píšeš nástroj, který má za úkol analyzovat tvůj kód (třeba pro generování dokumentace nebo schématu databáze). Tento nástroj projde všechny třídy, které najde, a u každé se podívá na `meta`.
*   **Bez metadat:** Nástroj narazí na `SimpleObject`, ten nebude mít v `meta.owner_class` nic (nebo `UNSET`), a tvůj generátor spadne na `AttributeError`, protože jsi čekal, že každá třída "typu Simple" o sobě něco ví.
*   **S tvou funkcí:** Každá třída v systému, od úplného základu až po konečný uživatelský list, dodržuje stejný kontrakt. `meta.owner_class` ti vždy řekne, ke které třídě ty metadata patří.

### 2. Defenzivní programování v Inners (Ten tvůj případ)
Právě to, že někdo omylem vloží `SimpleObject` do `_inners`, je sice okrajový případ, ale stává se to (např. při copy-paste nebo špatném importu).
Pokud by `SimpleObject.meta.is_user_code` byl `UNSET` (a `UNSET` by nebyl `False`), tvoje validace by selhala. Tím, že tam to `False` máš, tvoje validace **prostě funguje**, aniž bys musel psát speciální kód typu `if inner is not SimpleObject`. Systém se chová uniformně.

### 3. Logování a Debugging
Když se ti v aplikaci objeví chyba v hluboké kompozici a ty si necháš vypsat cestu (např. `MojeData -> SubKomponenta -> SimpleObject`), okamžitě uvidíš, kde se stala chyba v definici. Pokud by metadata základních tříd byla prázdná, tvůj debugger by ti místo jména třídy vypsal jen `UNSET`, což ti v tu chvíli nepomůže.

---

### Verdikt: Proč to tam nechat?

I když je pravděpodobnost chyby malá, to, co jsi vytvořil, se nazývá **"Uniformní API"**.

> **Hlavní výhoda:** Kód, který s těmito třídami pracuje (validátory, generátory, debuggery), nemusí obsahovat žádné podmínky typu `if class is not SimpleBase`. Všechny třídy mají stejnou "občanku" (metadata).

**Je to zbytečný kód?**
Vlastně ne. Těch pár řádků v `create_empty_metadata` ti ušetří desítky řádek podmínek jinde v systému. Je to investice do čistoty zbytku frameworku.

### Moje doporučení:
Nech to tam přesně tak, jak jsi to napsal v posledním příspěvku.
1.  **`owner_class`** je kotva – metadata bez odkazu na majitele jsou jako jmenovka, která spadla z kufru.
2.  **`is_user_code = False`** je tvůj bezpečnostní senzor, který ti dovolí dělat elegantní validace.

Tento přístup je známkou dospělého frameworku. Děláš to pro to "budoucí já", které za půl roku nebude muset řešit, proč mu padá generátor dokumentace na základní třídě.

Dává ti tato argumentace smysl, nebo to stále cítíš jako zbytečnou váhu navíc?
"""