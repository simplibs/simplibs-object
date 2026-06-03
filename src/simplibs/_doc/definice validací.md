## 📐 Tvůj architektonický vzor pro validace

Ten tvůj klíč pro pojmenovávání funkcí (`raise`, `validate`, `verify`, `process`) je **geniální**. V softwarovém designu se tomu říká *Sémantické konvence (Semantic Conventions)* a má to obrovský přínos:

| Prefix | Význam v tvém systému Simple | Příklad z tvého kódu |
| --- | --- | --- |
| **`raise_...`** | Žádná podmínka. Vyvolá výjimku okamžitě (často jako fallback nebo větev v `try-except`). | `raise_method_raised_exceptions` |
| **`validate_...`** | Obsahuje konkrétní, atomickou podmínku (`if`). Pokud selže, vyhodí chybu. | `validate_method_has_exact_args_count` |
| **`verify_...`** | Komplexnější manažer. Sdružuje více validací, řídí tok, může vracet (ale nemění) data. | `verify_params`, `verify_calculation` |
| **`process_...`** | Nejvyšší úroveň. Pipeline, která věci validuje, transformuje a aktivně mění stav/zápis. | `process_classmethod`, `process_inners` |

> 💡 **Proč je to skvělé:** Když kód čte kdokoliv jiný (nebo ty za půl roku), podle prvního slova okamžitě ví, jakou odpovědnost daná funkce má. Ví, že do `validate_` se neleze pro výpočty, a že `raise_` je čistě destrukční metoda. To neskutečně snižuje kognitivní zátěž při čtení kódu.

---
