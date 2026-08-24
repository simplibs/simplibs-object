# 🧩 Co tvoje knihovna vlastně je  
Je to **systém pro vytváření deterministických, typově bezpečných, reaktivních objektů**, které se skládají z:

- **atomických konstant** (SimpleConstant)  
- **kompozic** (SimpleObject)  
- **mixins** (SimpleMixin), které přidávají chování jako lego kostky  

Celé to funguje jako **mini‑framework pro deklarativní modelování dat**, kde uživatel jen napíše třídu s `_type`, `_default`, `_inners`, `_logic`…  
a zbytek se stane automaticky.

---

# 🧠 Jak to funguje uvnitř (jednoduše řečeno)

## 1) **Deklarativní definice**
Uživatel napíše něco jako:

```python
class Age(SimpleConstant):
    _type = int
    _default = 20
```

nebo

```python
class Person(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"
```

A tím je hotovo — žádné psaní konstruktorů, žádné validace, žádné ruční kontroly.

---

## 2) **Metaclass SimpleMeta**
Když Python načítá třídu, SimpleMeta:

- zjistí, jestli je to konstanta nebo kompozice  
- vytvoří jí metadata  
- zvaliduje typy, defaulty, inners, logiku  
- připraví atomické nebo kompozitní instance třídy  
- zajistí write‑once chování (třída se po definici už nedá měnit)

Třída se tak stane **blueprintem** — stabilním, neměnným popisem objektu.

---

## 3) **Dynamická tvorba instancí**
Když uživatel zavolá:

```python
person = Person()
```

tak SimpleMeta:

- vybere správnou atom/composite instanční třídu  
- přidá mixiny  
- dynamicky vytvoří novou runtime třídu přes `type()`  
- vytvoří instanci  
- inicializuje ji  
- a tu runtime třídu zahodí (instance si nese vše potřebné)

Každá instance má:

- `_value` — aktuální hodnotu  
- `_owner` — rodiče v kompozici  
- `_locked` — pro immutabilitu  
- properties pro inners  
- reaktivní metody `_recalculate_self` a `_recalculate_inners`

---

## 4) **Reaktivita**
Tady je kouzlo.

### 🔼 Když se změní hodnota uvnitř (atom):
- atomický setter `_root_value_setter` normalizuje hodnotu  
- uloží ji  
- zavolá `_owner._recalculate_self()`  
- tím se přepočítá celá kompozice směrem nahoru

### 🔽 Když se změní hodnota kompozice:
- `_recalculate_inners` zavolá `_decompose`  
- rozbije hodnotu na části  
- pošle je do jednotlivých innerů  
- a pokud jsou to další kompozice, pokračuje dál

Výsledek je **obousměrná reaktivita**, podobná tomu, co dělají:

- React (state → UI)  
- databázové ORM (model → children)  
- FRP systémy (Functional Reactive Programming)

Ale tady je to **deterministické, typově bezpečné, bez magie, bez runtime mutací třídy**.

---

# 🧱 K čemu se to dá použít

## 1) **Deklarativní datové modely**
Můžeš definovat datové struktury čistě deklarativně, bez psaní boilerplate.

## 2) **Validace a normalizace**
Každý objekt:

- má typ  
- má default  
- má validaci  
- má normalizaci  
- má metadata  
- má reaktivní chování  

To je ideální pro:

- konfigurace  
- formuláře  
- API payloady  
- DSL systémy  
- modelování doménových objektů  

## 3) **Reaktivní výpočty**
Když se změní část modelu, automaticky se přepočítá celek.

To je perfektní pro:

- finanční modely  
- matematické výpočty  
- simulace  
- stavové stroje  
- UI modely  

## 4) **Immutabilita + mixiny**
Mixiny umožňují přidávat:

- snapshoty  
- serializaci  
- kolekce  
- numerické operace  
- stepper logiku  
- vlastní chování  

A to vše **bez narušení jádra**.

---

# 🧩 Jak bych to popsal člověku, který o tom nikdy neslyšel

> „Je to knihovna, která ti umožní definovat datové objekty jen pomocí tříd, a ona za tebe udělá úplně všechno: validaci, typy, defaulty, reaktivitu, skládání objektů, immutabilitu, mixiny, a ještě ti vytvoří optimalizované instance.  
>  
> Je to jako kdybys měl vlastní mini‑jazyk pro modelování dat, ale napsaný v čistém Pythonu.“

---

# 🔥 A proč je to zajímavé
Protože:

- **uživatel píše jen deklaraci**, ne logiku  
- **vše je deterministické**  
- **vše je typově bezpečné**  
- **vše je reaktivní**  
- **vše je validované už při definici třídy**  
- **instance jsou extrémně lehké a rychlé**  
- **mixiny dávají neomezenou rozšiřitelnost**  
- **celý systém je modulární a atomický**

Je to vlastně **kombinace datových tříd, validátorů, reaktivního stromu a DSL**, ale udělaná tak, aby byla:

- čitelná  
- bezpečná  
- rozšiřitelná  
- predikovatelná  
- a hlavně příjemná pro vývojáře  

