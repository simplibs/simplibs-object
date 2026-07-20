Máš naprosto pravdu a plně s tebou souhlasím! Moje minulé já často nadává mému ještě staršímu já, že si do poznámek nezapsalo ten hluboký kontext, proč se věci dělaly zrovna takhle. U `_DESIGN_NOTES` nešetříme místem. Je to inženýrská studnice vědomostí pro chvíle, kdy se v tom kódu po roce někdo hrabe a snaží se pochopit celkový obraz, souvislosti a příklady.

Zde je kompletní přepis `_DESIGN_NOTES` pro `validate_class_name_is_identifier.py`, který do puntíku zachovává a rozšiřuje všechny původní myšlenky (včetně příkladů, garantovaných vlastností a celého řetězce validací), vše převedené do perfektní technické angličtiny.

---

### 📝 Aktualizované `_DESIGN_NOTES` (Kompletní hluboký kontext)

```python
_DESIGN_NOTES = """
# validate_class_name_is_identifier

## Purpose
This validation acts as a fundamental technical filter for class names. Its primary objective is to guarantee that the blueprint class name adheres strictly to Python's lexical definitions for identifiers before any other processing or name splitting occurs.

## Why This Validation Is Necessary (Dynamic Context)
While standard static definitions (e.g., `class MyClass:`) are checked natively by the Python parser/compiler, dynamic runtime class generation using `type("Invalid-Name", ...)` is highly permissive. It allows creating classes with names containing spaces, hyphens, dots, or names starting with digits. 
This function guarantees that even a dynamically spawned class possesses an executable-safe identity name that is technically usable for downstream attribute generation and dynamic code evaluation.

## Validation Pipeline Architecture
Within the metadata initialization sequence, this check serves as the initial guardian before finer filtering takes place. The architectural processing flow follows these three distinct pillars:
1. `validate_class_name_is_identifier` (This function): Eliminates spaces, hyphens, dots, and starting digits. Allows: `[a-zA-Z0-9_]` (including valid Unicode word/diacritic characters).
2. `validate_class_name_is_ascii`: Eliminates localized diacritics and non-ASCII Unicode letters. Allows: `[a-zA-Z0-9_]`.
3. `validate_class_name_has_no_underscores`: Eliminates underscores entirely, establishing a pure PascalCase constraint. Allows: `[a-zA-Z0-9]`.

## Native Python Guarantees
Even during dynamic class creation via `type()`, the Python runtime natively ensures the following (raising TypeError or ValueError automatically before this validation is even reached):
- The incoming class name attribute is always a strict `str` type.
- The incoming string is never an empty value `""`.

## Examples
```python
# VALID (Passes this check, diacritics/underscores handled downstream)
validate_class_name_is_identifier("MyClass")               # OK
validate_class_name_is_identifier("Třída_1")               # OK

# INVALID (Raises SimpleMetadataError via ValueError)
validate_class_name_is_identifier("123Class")              # Fail: starts with a digit
validate_class_name_is_identifier("My-Class")              # Fail: contains a hyphen
validate_class_name_is_identifier("My Class")              # Fail: contains a space
validate_class_name_is_identifier("My.Class")              # Fail: contains a dot

```

"""

```

---

---

## ⚖️ Velká debata: `@pytest.mark.parametrize` vs. `subtests` v cyklu

Tohle je skvělé téma. Oba přístupy řeší stejný problém (testování více vstupů proti jedné logice), ale každý k němu přistupuje z úplně jiného směru. Pojďme si je rozebrat podle kritérií, která při psaní robustních knihoven rozhodují.

### 1. `@pytest.mark.parametrize` (Pytest Standard)
Tento dekorátor vezme vstupní matici a vygeneruje z ní **samostatné nezávislé testy** ještě před spuštěním testovací suity.

*   **Výhody:**
    *   **Maximální izolace:** Když selže 3. vstup ze 100, pytest ho ukáže jako jeden konkrétní selhaný test. Ostatních 99 normálně projde.
    *   **Čistota reportu:** Každý řádek matice dostane v konzoli své vlastní ID (např. `test_identifier[123Class-starts with a digit]`).
    *   **Kompatibilita s IDE:** V PyCharmu nebo VS Code můžeš kliknout na to jedno konkrétní selhání a spustit znovu *jen ten jeden specifický vstup*.
*   **Nevýhody:**
    *   **Statický kontext:** Všechna data v matici se vyhodnocují v době načítání testů. Nemůžeš v matici snadno reflektovat dynamický runtime stav.
    *   **Vizuální šum u komplexních objektů:** Pokud testuješ obří slovníky nebo struktury, dekorátor nad funkcí začne opticky bobtnat a kód testu se odsouvá dolů.

### 2. Cyklus s `subtests` (Kontextový přístup)
Tento přístup běží uvnitř **jednoho jediného testu**, který pomocí kontext manažeru zachytává selhání bez přerušení cyklu[cite: 3].

*   **Výhody:**
    *   **Dynamická reflexe (Klíčové pro nás!):** Matici dat můžeš vygenerovat dynamicky přímo v těle testu na základě aktuálního stavu systému (přesně jako to dělala ukázka s `SettingsMeta._VALIDATORS`).
    *   **Lokalita kódu:** Data (matice) i exekuce (`assert_exception_function`) leží hned vedle sebe uvnitř těla funkce.
    *   **Atomická celistvost:** Z pohledu Pytestu testuješ *jedno téma* (např. nevalidní vstupy) jako jeden logický blok.
*   **Nevýhody:**
    *   Pokud nepoužiješ kontext manažer `subtests` správně (nebo ho vynecháš), první chyba utne celý zbytek cyklu a ty nevíš, jestli by ostatní vstupy prošly. (S pluginem `pytest-subtests` je to ale ošetřené[cite: 3]).

---

### 🛠️ Moje inženýrské doporučení: Kdy co použít?

1.  **Kdy použít `@pytest.mark.parametrize`:**
    *   Když testuješ čisté matematické/transformační funkce (např. náš `class_name_splitter`[cite: 4] — pošleš string, čekáš tuple). Vstupy jsou statické, jasné a nezávislé.
2.  **Kdy použít cyklus s `subtests`:**
    *   **Když testujeme chybové stavy a výjimky pomocí orchestrátorů (`assert_exception_function`).** Tyto orchestrátory interně provádějí spoustu sub-assertů (kontrolují label, expected, how_to_fix...)[cite: 4]. Balení tohoto celého kolosu do obřího dekorátoru nad funkcí často vede k méně čitelnému kódu.
    *   Když potřebuješ vstupy reflektovat dynamicky (např. testování povolených klíčů, které se tahají ze třídy za běhu).

Pro naše validační raisery je formát s `subtests` v těle testu extrémně čistý, protože drží exekuci `assert_exception_function` pohromadě s testovací maticí[cite: 4].

Jak se ti líbí tato hluboká verze designových poznámek? Můžeme postoupit k `validate_class_name_is_ascii.py`? 🚀

```