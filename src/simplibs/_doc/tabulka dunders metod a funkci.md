To je skvělý nápad\! Abychom mohli dělat "chirurgické" zásahy do metod, musíme přesně vědět, kde leží která "tepna" nebo "nerv" v jejich struktuře. Python si o každé funkci/metodě ukládá obrovské množství informací v takzvaných **Dunder (Double Under) atributech**.

Zde je mapa objektu "Funkce" (nebo "Metoda"), která ti odhalí vše, co Python vidí.

### 1\. Mapa Funkčního Objektu (Dunder Anatomy)

Zde je tabulka klíčových atributů. Nejdůležitější pro nás je `__code__`, což je v podstatě "mozek" funkce, a pak "paměťové" atributy pro defaulty.

| Atribut | Co reprezentuje (Popis) | Pod-přihrádky (Co v nich najdeme) |
| :--- | :--- | :--- |
| **`__code__`** | **Objekt bajtkódu.** Statický popis struktury funkce (to, co Python vyčetl při kompilaci souboru). | `co_argcount`: Počet pozičních parametrů.<br>`co_kwonlyargcount`: Počet keyword-only parametrů.<br>`co_varnames`: Názvy všech lokálních proměnných (včetně parametrů).<br>`co_flags`: Bitové příznaky (např. zda má `**kwargs` nebo je to generátor).<br>`co_consts`: Všechny konstanty použité uvnitř těla (např. čísla, stringy). |
| **`__defaults__`** | **Výchozí hodnoty pozičních parametrů.** | Tuple hodnot (např. `(10, "A")`). Pokud nejsou, je zde `None`. |
| **`__kwdefaults__`** | **Výchozí hodnoty keyword-only parametrů.** | Slovník (Dict), kde klíčem je název parametru a hodnotou default. |
| **`__annotations__`** | **Typové anotace.** | Slovník mapující jména parametrů na typy (např. `{'value': Any}`). |
| **`__doc__`** | **Docstring.** Dokumentační řetězec funkce. | String (např. `"Nepovinná doplňková validace."`). |
| **`__signature__`** | **Umělá signatura.** Standardně neexistuje (vrací ji až `inspect.signature`). | Pokud ji tam sami vložíme, přepíšeme tím "vývěsku" pro okolní svět. |
| **`__func__`** | **Původní funkce.** (Pouze u `@classmethod` nebo `@staticmethod`). | Odkazuje na čistou funkci "pod" dekorátorem. |
| **`__self__`** | **Vázaný objekt.** (Pouze u `@classmethod` nebo metod instancí). | U `@classmethod` zde najdeme samotnou třídu (náš `cls`). |

* **Co dalšího je v `co_flags`?** Je to bitové pole, které říká interpretu, jak s funkcí zacházet:
    * `0x01`: Funkce byla optimalizována (téměř vždy).
    * `0x02`: Nové lokální proměnné (téměř vždy).
    * `0x04`: Přítomen `*args` (variabilní poziční argumenty).
    * **`0x08`**: Přítomen `**kwargs`.
    * `0x20`: Funkce je generátor (obsahuje `yield`).
    * `0x80`: Funkce je korutina (`async def`).

**Logika je tedy v: `method.__code__.co_code`**

| Přihrádka v `__code__` | Co v ní skutečně je |
| :--- | :--- |
| **`co_code`** | **Logika (Bytecode)** – Sled instrukcí, co se má dělat. |
| **`co_consts`** | **Skladiště hodnot** – Všechna čísla a stringy napsané "natvrdo" v kódu. |
| **`co_varnames`** | **Seznam jmen** – Jména proměnných, na která se odkazuje `co_code` pomocí indexů. |

Toto jsou všechna pole, která Python ukládá do objektu bajtkódu. Bez nich by „stroj“ neexistoval.

| Pole (Atribut) | Typ | Význam pro „Stroj“ a autora |
| :--- | :--- | :--- |
| **`co_code`** | `bytes` | **Srdce (Logika):** Samotná sekvence instrukcí (opcodes). Tady je „příkazový řetězec“ toho, co se má dít. |
| **`co_consts`** | `tuple` | **Konstanty:** Všechny hodnoty (čísla, řetězce, None), které jsou v kódu zapsány natvrdo. První prvek je často docstring. |
| **`co_names`** | `tuple` | **Globální jména:** Názvy, které nejsou lokální v této funkci (např. volání jiných funkcí, globální proměnné, atributy jiných objektů). |
| **`co_varnames`** | `tuple` | **Lokální proměnné:** Jména parametrů a proměnných vytvořených uvnitř funkce. |
| **`co_argcount`** | `int` | **Počet pozičních argumentů:** Kolik slotů z `co_varnames` je vyhrazeno pro základní parametry. |
| **`co_posonlyargcount`** | `int` | **Počet pozičně-pouze argumentů:** Parametry před `/` v definici. |
| **`co_kwonlyargcount`** | `int` | **Počet keyword-only argumentů:** Parametry po `*` v definici. |
| **`co_nlocals`** | `int` | **Počet lokálních jmen:** Celkový počet položek v `co_varnames`. |
| **`co_stacksize`** | `int` | **Hloubka zásobníku:** Maximální množství dat, které si Python musí „držet v ruce“ během provádění jedné instrukce. |
| **`co_flags`** | `int` | **Vlastnosti (Příznaky):** Bitové pole (0x04 pro `*args`, 0x08 pro `**kwargs`, 0x20 pro generátory atd.). |
| **`co_filename`** | `str` | **Původ:** Cesta k `.py` souboru, kde kód vznikl. |
| **`co_name`** | `str` | **Jméno:** Název funkce nebo metody. |
| **`co_firstlineno`** | `int` | **Start:** Číslo prvního řádku funkce v souboru. |
| **`co_lnotab`** | `bytes` | **Line Number Table:** Tabulka, která říká: „Tyto bajty v `co_code` odpovídají tomuto řádku v souboru.“ Klíčové pro debugging. |
| **`co_freevars`** | `tuple` | **Volné proměnné:** Jména proměnných z nadřazeného rozsahu (pro uzávěry/closures). |
| **`co_cellvars`** | `tuple` | **Buňkové proměnné:** Jména lokálních proměnných, na které odkazují vnitřní vnořené funkce. |

-----

### 2\. Srovnání: SimpleObject vs. Uživatel vs. Metadata

Pojďme si porovnat tři různé pohledy na tutéž metodu `_validate`. Předpokládejme, že uživatel definoval:

```python
@classmethod
def _validate(cls, hodnota, **moje_kwargs):
    return True
```

#### A) `SimpleObject._validate` (Základní vzor)

Toto je naše "tovární" nastavení.

  * **`__defaults__`**: `None` (nemáme žádné poziční defaulty).
  * **`__kwdefaults__`**: `{'return_bool': False}` (protože `return_bool` je za hvězdičkou).
  * **`co_varnames`**: `('cls', 'value', 'return_bool')`.
  * **`co_flags`**: Neobsahuje příznak pro `**kwargs`.

#### B) `self.owner_class._validate` (Uživatelská definice)

Toto je to, co uživatel napsal. Python to "vytáhl" ze souboru.

  * **`__defaults__`**: `None`.
  * **`__kwdefaults__`**: `None` (uživatel ho v definici nepoužil).
  * **`co_varnames`**: `('cls', 'hodnota', 'moje_kwargs')`.
  * **`co_flags`**: **Má nastaven bit 0x08 (`CO_VARKEYWORDS`)**, protože uživatel použil `**moje_kwargs`.
  * **`__self__`**: Odkazuje na `MojeTrida`.

#### C) `self.validate` (Atribut v tvých metadatech)

Zde se děje ta magie. Ve chvíli, kdy v `initu` metadat uděláš `self.validate = owner_class._validate`, stane se toto:

1.  **Identita**: `self.validate` je v podstatě jen další "ukazatel" na stejný objekt jako `owner_class._validate`. Mají stejné `__code__`, `__defaults__` i `__self__`.
2.  **ALE...** ve chvíli, kdy uděláš:
    `self.validate.__signature__ = get_signature(SimpleObject._validate)`
    ...tak **změníš tento objekt u obou**. Protože v Pythonu jsou funkce objekty předávané referencí, změna `self.validate.__signature__` se projeví i na `owner_class._validate`.

-----

### 3\. Co z toho plyne pro tvůj ZEN?

Teď už vidíš, proč tvá včerejší úvaha o "přetížení" signatury nestačila:

1.  **Strojovna (`__code__`) je neměnná:** Když uživatel napíše `def _validate(cls, value):`, tak v `co_varnames` jsou prostě jen dva sloty. I když mu na dveře (přes `__signature__`) nalepíš ceduli "Tady přijímáme i return\_bool", ten procesor uvnitř o tom neví a jakmile tam ten parametr pošleš, zahlásí chybu.
2.  **Defaulty jsou rozdělené:** Pokud chceš v metodě `_logic` používat defaulty z `inners`, musíš je "vstříknout" do `__defaults__`. Bez toho bude Python tvrdit, že mu chybí argumenty.
3.  **Sdílený osud:** Když v metadatech "vylepšuješ" metodu (např. jí měníš signaturu nebo anotace), děláš to přímo na té metodě, která patří té třídě. To je dobře\! Znamená to, že kdokoliv jiný (třeba Swagger, dokumentace nebo jiný vývojář) se zeptá té třídy na její `_validate`, dostane tu tvoji krásně "orazítkovanou" verzi.

### Proč Python takto odděluje `__code__` a `__signature__`?

Protože bajtkód (`__code__`) je "zmrazený" a velmi rychlý pro procesor. Signatura je "pomalá", lidsky čitelná a flexibilní věc pro nás lidi.

**Pomohlo ti toto srovnání v tabulce a výklad dunderů k tomu, aby se ti ta mapa v hlavě složila?** Teď už víš, kam přesně sáhnout, když budeš chtít změnit chování (to je `__defaults__` a `__kwdefaults__`) a kam sáhnout, když chceš změnit jen vzhled (`__signature__` a `__annotations__`). 🐾