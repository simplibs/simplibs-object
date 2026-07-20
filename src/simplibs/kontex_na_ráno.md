Rozumím ti na sto procent. Ta domýšlivost (halucinace) je u AI modelů klasická vlastnost, ale u ladění precizního hodinového strojku, jako je `SimpleObject`, nemá co dělat. Zde platí **absolutní inženýrská přesnost a nulová tolerance pro odhady**.

Pokud mi jakýkoli kousek skládačky (kód, vazba, typ) bude chybět, rovnou si o něj řeknu. A pokud v nějakém specifickém scénáři nabídnu hypotézu, jasně a viditelně tě na to upozorním větou: *„Pozor, zde odhaduji...“*

Zde je naše kompletní kotva a rekapitulace kontextu, kterou si můžeme kdykoli (třeba zítra ráno) nahrát pro okamžité naladění na stejnou vlnu:

---

# ⚓ CONTEXT ANCHOR: SimpleObject Refactoring & Testing

## 1. Architektura knihovny (Deterministický design)

Knihovna staví robustní, uzavřený systém postavený na dvou klíčových stavebních kamenech, kde validace integrity probíhá striktně **při inicializaci třídy/metadat**, nikoli až ex-post nad hotovou instancí:

* **`SimpleConstant`:** Reprezentuje atomické, pevné hodnoty s typovou kontrolou. Definuje vnitřní rozhraní (`_type`, `_default`, `_validate`) a vnější rozhraní (`validate_type`, `validate`, `is_valid`, `normalize`).
* **`SimpleObject`:** Dědí z `SimpleConstant`. Umožňuje vytvářet kompozice složené z konstant nebo jiných objektů. Definuje vnitřní rozhraní pro kompoziční logiku (`_inners`, `_logic`, `_decompose`) a vnější rozhraní pro práci s nimi (`calculate_value` s podporou `ParamSpec` pro IDE, `decompose_value`).

## 2. Cíl a rozsah práce

Aktuálně finalizujeme kód do produkčního stavu (příprava pro GitHub a PyPI). Práce je rozdělena na dvě fáze:

* **Fáze 1 (Výjimky):** Zpracování a otestování základních tříd výjimek v `src/simplibs/object/exceptions` (`SimpleError`, `SimpleLogicError`, `SimpleMetadataError`, `SimpleMixinError`).
* **Fáze 2 (Validační logiky):** Postupný překlad, pročištění a implementace atomických validačních funkcí napříč celou strukturou `_core_logic` (včetně následného dopisování chybějících mixinových validací).

## 3. Pravidla pro psaní kódu a dokumentace

* **Striktní angličtina (Zero Czech Policy):** Všechny docstringy, komentáře a designové poznámky tvoříme výhradně v čisté, profesionální technické angličtině. V kódu nesmí zůstat ani stopa po češtině.
* **Koncept `_DESIGN_NOTES`:** Každý soubor končí textovým blokem `_DESIGN_NOTES`. Tento blok slouží jako rozšířená dokumentace vysvětlující **proč** a **jak** (záměr, kontext, architektura). Popisuje výhradně **aktuální stav kódu**, nikoli historii změn.

## 4. Testovací strategie (`testing` framework)

Testy píšeme v atomickém stylu (jeden testovací soubor přesně odpovídá jednomu zdrojovému souboru) za použití dvou orchestrátorů postavených na vzoru Facade:

* **`assert_exception_class`:** Pro testování tříd výjimek (ověření dědičnosti a dunder metod).


* **`assert_exception_function`:** Pro testování validačních funkcí (ověření Happy Path a generování správně strukturovaných výjimek pomocí substring matchingu).



---

Kotva je nahozená, pravidla hry jsou jasně nastavená. Až budeš chtít začít (ať už teď, nebo zítra ráno), stačí poslat první soubor výjimky ze složky `exceptions/` a jdeme na to! 🚀
