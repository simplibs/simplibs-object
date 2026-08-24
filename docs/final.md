
---

### 🏛️ Základní stavební kameny: `SimpleConstant` & `SimpleObject`

Jádro knihovny stojí na dvou základních deklarativních třídách sdílejících společný základ `SimpleBase`. Umožňují modelovat data od nejmenších atomických jednotek až po rozsáhlé reaktivní stromy bez psaní zbytečného kódu (boilerplate).

```
                      ┌─────────────────────────┐
                      │       SimpleBase        │ ◄── Společný základ, metadatová vazba
                      └────────────┬────────────┘
                                   │
                  ┌────────────────┴────────────────┐
                  ▼                                 ▼
       ┌────────────────────┐            ┌────────────────────┐
       │   SimpleConstant   │            │    SimpleObject    │
       │  (Atomická hodnota)│            │ (Složená kompozice)│
       └────────────────────┘            └────────────────────┘

```

#### 1. `SimpleConstant` (Atomická jednotka)

Slouží k reprezentaci jediné konkrétní hodnoty (číslo, řetězec, stav). Definuje typ (`_type`), výchozí hodnotu (`_default`) a volitelnou normalizační či validační logiku (`_validate`). Jakmile hodnotu změníte v rámci kompozice, automaticky probudí a přepočítá nadřazený objekt.

➡️ [docs/core/README_SIMPLE_CONSTANT.md](https://www.google.com/search?q=https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_CONSTANT.md)

#### 2. `SimpleObject` (Složená kompozice)

Představuje uzel složený z více vnitřních prvků (`_inners`). Tyto vnitřní prvky mohou být jak konstanty (`SimpleConstant`), tak další objekty (`SimpleObject`). Definuje transformační pravidlo směrem nahoru (`_logic`) i zpětný rozpad směrem dolů (`_decompose`), čímž zajišťuje plně reaktivní obousměrný datový tok.

➡️ [docs/core/README_SIMPLE_OBJECT.md](https://www.google.com/search?q=https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_OBJECT.md)

#### 3. `SimpleBase` (Společná infrastruktura)

Abstraktní základní třída zajišťující jednotné propojení s metatřídou `SimpleMeta`. Garantuje neměnnost třídní definice (write-once blueprint), generování instančních struktur a přístup k interním metadatům.

➡️ [docs/core/README_SIMPLE_BASE.md](https://www.google.com/search?q=https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_BASE.md)

---

