# 🧱 `SimpleBase` — Kořen celé hierarchie

`SimpleBase` je nejnižší patro celého Simple systému. Sama o sobě nic nedělá —
jejím jediným úkolem je dát všem deklarativním třídám (`SimpleConstant`,
`SimpleObject`) společnou identitu a napojit je na metaclassu `SimpleMeta`,
která teprve vdechne život skutečnému chování.

```
SimpleBase            (metaclass=SimpleMeta, žádná deklarativní logika)
└── SimpleConstant    (atom: _type, _default, _validate)
    └── SimpleObject  (kompozice: _inners, _logic, _decompose)
```

---

## 🧭 Obsah

* [Proč tahle třída vůbec existuje](#proč-tahle-třída-vůbec-existuje)
* [`__slots__`](#__slots__)
* [`__metadata__`](#__metadata__)
* [Architektonická role](#architektonická-role)

---

## Proč tahle třída vůbec existuje

Bez `SimpleBase` by musela `SimpleConstant` i `SimpleObject` samostatně řešit
napojení na `SimpleMeta` a musely by si každá zvlášť definovat placeholder pro
metadata. Tím, že je tohle vytažené do společného kořene, má celý systém jeden
jediný bod, ve kterém se historicky rozhoduje "od teď je každá třída v této
hierarchii Simple třída" — a tenhle bod se nikdy nemusí měnit.

```python
class SimpleBase(metaclass=SimpleMeta):
    __slots__ = ()
    __metadata__: "SimpleMetadataLike" = UNSET
```

Třída se **nepoužívá přímo** — neexistuje scénář, kdy bys dědil rovnou ze
`SimpleBase`. Je to čistě architektonický "kotevní bod", ne funkční stavební
kámen.

[▲ Nahoru](#-obsah)

---

## `__slots__`

```python
__slots__ = ()
```

Prázdný slot tuple neznamená "žádná data" — znamená "žádná *vlastní* data".
`SimpleBase` jen garantuje, že se do hierarchie od začátku nedostane `__dict__`
(a s ním neomezené, nekontrolované přidávání atributů za běhu). Každá
podtřída musí definovat svoje vlastní `__slots__`, aby si tuhle výhodu
zachovala — `SimpleBase` sama o sobě ji jen nastavuje jako výchozí standard.

Přínos je čistě výkonnostní a paměťový: menší instance, rychlejší přístup
k atributům, předvídatelný layout v paměti.

[▲ Nahoru](#-obsah)

---

## `__metadata__`

```python
__metadata__: "SimpleMetadataLike" = UNSET
```

Tohle je placeholder, ne skutečná hodnota. `SimpleBase` (a systémové třídy
obecně) žádná metadata nemají a mít nepotřebují — `UNSET` tu jen garantuje,
že atribut `__metadata__` **existuje** na každé třídě v hierarchii, i než ho
`SimpleMeta.__new__` doplní skutečnými, vypočítanými metadaty pro konkrétní
uživatelskou deklarativní třídu.

Díky tomu může zbytek systému bezpečně předpokládat "`__metadata__` na téhle
třídě existuje", aniž by musel řešit `AttributeError` na okrajích hierarchie.

[▲ Nahoru](#-obsah)

---

## Architektonická role

`SimpleBase` shrnutě:

* sjednocuje dědičnost — jeden společný předek pro atomy i kompozice,
* dává stabilní kotvu pro chování metaclassy,
* garantuje, že každá Simple třída sdílí stejný strukturální základ
  (sloty, přítomnost `__metadata__`).

Je to "kořenový uzel" celého Simple ekosystému — záměrně minimální, aby
nezanášel veřejné API ničím zbytečným. Veškeré skutečné chování je
definované až v `SimpleConstant`, `SimpleObject` a v samotné `SimpleMeta`.

➡️ Pokračování: [README_SIMPLE_CONSTANT.md](README_SIMPLE_CONSTANT.md)

[▲ Nahoru](#-obsah)
