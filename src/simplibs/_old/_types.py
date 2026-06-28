from typing import TypeAlias
from types import EllipsisType, TracebackType
from collections.abc import Callable, Mapping
from datetime import datetime
from typing import Any, Self, Type


# ----------------------------------------------------
# Tuple
# ----------------------------------------------------

# Logika řazení podskupin:
#
# tuple[str, ...] — nejkonkrétnější homogenní
# tuple[X, ...] — homogenní, jiný typ
# tuple[Any, ...] — homogenní, volný typ
# tuple[str, X] — fixní dvojice/trojice začínající str
# tuple[X, Y] — fixní dvojice jiného typu
# Union obsahující tuple
# Složená fixní struktura

# tuple[str, ...]
# -------------------------

# N-tice názvů všech registrovaných prvků
NamesTuple: TypeAlias = tuple[str, ...]

# Reprezentuje hierarchickou sémantickou cestu k prvku (např. ("parent", "sub_node"))
PathTuple: TypeAlias = tuple[str, ...]

# N-tice textových názvů parametrů pro metodu _logic
NamesTuple: TypeAlias = tuple[str, ...]


# tuple[X, ...]  (homogenní n-tice jiného typu)
# -------------------------

# Celkový sekvenční registr všech sub-node prvků kompozice
NodesTuple: TypeAlias = tuple[NodeItem, ...]

# Reprezentuje n-tici mixinů aplikovaných na danou instanci nebo třídu
MixinsTuple: TypeAlias = tuple["SimpleMixinLike", ...]

# Reprezentuje n-tici vnitřních komponent deklarovaných v kompozici
InnersTuple: TypeAlias = tuple["SimpleClassLike", ...]



# tuple[str, X]  (dvojice začínající str)
# -------------------------

# Jedna dvojice reprezentující změnu (název_prvku, nová_hodnota)
ConstantChange: TypeAlias = tuple[str, Any]


# tuple[X, Y]  (dvojice jiného typu)
# -------------------------

# Jedna položka v registru: dvojice (živá_instance, její_cesta)
NodeItem: TypeAlias = tuple["SimpleInstanceLike", "PathTuple"]


# Union obsahující tuple
# -------------------------

# Komplexní vstup pro hromadné změny: buď jedna dvojice, n-tice dvojic, nebo nic
ConstantChanges: TypeAlias = ConstantChange | tuple[ConstantChange, ...] | None

# ----------------------------------------------------
# Dict
# ----------------------------------------------------

# Logika řazení podskupin:
#
# dict[str, Any] — nejčastější vzor, volná hodnota
# dict[str, Any] | None — stejný vzor, ale nullable
# dict[str, X] — konkrétní typ hodnoty
# dict[X, Any] — jiný typ klíče

# dict[str, Any]
# -------------------------

# Slovník mapující názvy prvků na jejich nové hodnoty pro hromadnou aktualizaci
ChangesDict: TypeAlias = dict[str, Any]

# Reprezentuje plochý slovník se serializovanými daty/stavem objektu
StateDict: TypeAlias = dict[str, Any]


# dict[str, X]  (konkrétní hodnota)
# -------------------------

# Rychlá mapa pro vyhledání vnitřní třídy podle jejího snake_case jména
InnersMap: TypeAlias = dict[str, "SimpleClassLike"]


# ----------------------------------------------------
# Mapping
# ----------------------------------------------------

# Komplexní mapa propojující snake_case název uzlu s jeho živou instancí a cestou
NodesDict: TypeAlias = Mapping[str, tuple["SimpleInstanceLike", PathTuple]]

# Rychlá mapa pro přímý přístup k živé instanci sub-nodu podle jeho snake_case názvu
NodesInstanceDict: TypeAlias = Mapping[str, "SimpleInstanceLike"]

# Mapa přiřazující snake_case názvu poduzlu jeho relativní hierarchickou cestu
NodesPathDict: TypeAlias = Mapping[str, PathTuple]

# Indexová mapa určující přesné pořadí pozice sub-nodu v původní sekvenci
NodesIndexMap: TypeAlias = Mapping[str, int]


# ----------------------------------------------------
# Scalar / Union / Other
# ----------------------------------------------------

# Reprezentuje akceptovatelné typové definice (např. int nebo int | str)
ValidTypes: TypeAlias = type | UnionType