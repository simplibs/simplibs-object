Tato struktura je z pohledu systémové čistoty vynikající. Rozděluje odpovědnosti přesně podle toho, co daný prvek v systému představuje, a odstraňuje „rozdvojenou osobnost“ objektů, které se snažily být zároveň atomem i kompozicí.

Zde je rozpis této architektury, zaměřený na **metadata** a **životní cyklus definice třídy**.

---

### 1. Úroveň Tříd (Veřejné rozhraní)

Zde definujeme, co vývojář píše do kódu.

* **`SimpleBase`**: Obsahuje pouze to, co je společné všem (např. přístup k `.meta`, základní metody pro validaci, které jsou univerzální). Neobsahuje definici `_type` ani `_inners`.
* **`SimpleConstant(SimpleBase)`**: Přidává atributy pro hodnotu: `_type` a `_DEFAULT`. Je to konečný bod (Leaf).
* **`SimpleObject(SimpleBase)`**: Přidává atributy pro kompozici: `_inners`, `_logic` a `_decompose`. Je to uzel (Node).

---

### 2. Úroveň Metatřídy (`SimpleMeta`)

Tato třída funguje jako **inteligentní třídička**.

* **Role**: V metodě `__new__` prozkoumá `namespace` nově vznikající třídy.
* **Logika**:
    * Pokud vidí `_inners`, přiřadí `SimpleObjectMetadata`.
    * Pokud nevidí `_inners` (a jde o potomka `SimpleConstant`), přiřadí `SimpleConstantMetadata`.
    * Pro samotné bázové třídy (`SimpleBase`) přiřadí `SimpleBaseMetadata` (aby se zabránilo chybám při přístupu k `.meta`).

---

### 3. Úroveň Metadatových Procesorů (Střeva)

Zde dochází k největšímu zpřesnění. Použijeme dědičnost orchestrátorů tak, aby každý dělal jen svou práci.

#### **`SimpleBaseMetadata`**
Základní kámen, který řeší identitu prvku.
* **Data**: `owner_class`, `name_snake`, `name_title`, `name_readable`, `name_private`.
* **Procesory**: Pouze `create_names`.
* **Význam**: Každý prvek v systému musí mít jméno, ať je to konstanta nebo kompozice.

#### **`SimpleConstantMetadata(SimpleBaseMetadata)`**
Specialista na hodnotu a typ.
* **Data z baze**: (všechna jména).
* **Nová data**: `value_type`, `default`, `validate_method`, `atom_param_signature`.
* **Procesory**: `process_type`, `process_default_for_constant`, `process_validate_method`.
* **Využití**: Slouží jako základní stavební blok (Atom) pro kompozice.

#### **`SimpleObjectMetadata(SimpleBaseMetadata)`**
Specialista na vztahy a transformace.
* **Data z baze**: (všechna jména).
* **Nová data**: `inners`, `logic`, `decompose`, `logic_signature`, `decompose_signature`, `output_type`.
* **Procesory**: `process_inners`, `process_logic`, `process_decompose`.
* **Poznámka**: Tato třída **nedědí** ze `SimpleConstantMetadata`, protože kompozice nepotřebuje `_DEFAULT` (její hodnota vzniká výpočtem z částí).

---

### Schéma toku dat v Metadatech



### Proč je toto rozdělení "Zenové"?

1.  **Striktní Typizace**: V `SimpleConstantMetadata` víš, že `value_type` je povinný. V `SimpleObjectMetadata` víš, že typ může být odvozen z návratové hodnoty `_logic`. Nemusíš v kódu psát nekonečné `if self.is_composition:`.
2.  **Oddělení Validací**:
    * Validace pro Konstanty řeší shodu `default` vs `type`.
    * Validace pro Objekty řeší shodu `logic` parametrů vs `inners`.
    * Každý orchestrátor má svůj vlastní, čistý seznam validací v `__init__`.
3.  **Škálovatelnost**: Pokud v budoucnu přidáš např. `SimpleCollection` (seznam objektů), vytvoříš jen `SimpleCollectionMetadata`, které opět zdědí jména ze `SimpleBaseMetadata`, ale zbytek si vyřeší po svém.

### Zpracování v praxi (Pohled do budoucna)

Až budeš mít hotovou `SimpleObjectMetadata`, bude pro ni velmi snadné pracovat s `inners`, protože každý `inner` bude mít v sobě buď `SimpleConstantMetadata` nebo `SimpleObjectMetadata`. Díky tomu, že oba dědí z `SimpleBaseMetadata`, můžeš se spolehnout na to, že u každého z nich najdeš `name_snake`, což je klíčové pro tvou `logic_signature`.

Tato struktura je čistá, symetrická a dává každému kousku dat jasný domov. Chceš nyní prozkoumat nějakou konkrétní část tohoto rozdělení, nebo se cítíš připraven začít tyto tři větve metadat definovat?