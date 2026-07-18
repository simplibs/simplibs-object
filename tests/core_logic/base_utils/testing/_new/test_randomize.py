from __future__ import annotations

from typing import Any, TYPE_CHECKING, Callable
from types import UnionType
from collections.abc import Iterable
import random
import string
from datetime import datetime, date, timedelta
from pathlib import Path
from enum import Enum

if TYPE_CHECKING:
    from ....protocols.instance import SimpleInstanceLike
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.alias_typings import ValidTypes


# ---------------------------------------------------------
# Registr generátorů (uživatel může přidávat vlastní)
# ---------------------------------------------------------

TYPE_GENERATORS: dict[ValidTypes, Callable[[], Any]] = {}


def register_generator(type_: ValidTypes, func: Callable[[], Any]) -> None:
    """
    Umožní uživateli zaregistrovat vlastní generátor pro typ.

    - type_  → typ nebo UnionType (např. int, str, int | str)
    - func() → funkce bez argumentů vracející náhodnou hodnotu daného typu
    """
    TYPE_GENERATORS[type_] = func


# ---------------------------------------------------------
# Hlavní API – naplnění celé instance
# ---------------------------------------------------------

def fill_random(
    obj: "SimpleInstanceLike",
    *,
    retries: int = 5,
    allow_locked: bool = False,
) -> "SimpleInstanceLike":
    """
    Naplní Simple instanci náhodnými daty.

    - Rekurzivně projde celý strom (inners).
    - Pro atomy generuje hodnotu podle meta.value_type.
    - Respektuje validaci (validate / normalize).
    - Má retry mechanismus pro nevalidní hodnoty.
    - Pokud allow_locked=False, přeskočí zamčené prvky.
    """

    meta: "SimpleMetadataLike" = obj.meta

    # 1) Pokud má inners → rekurzivně naplníme vnitřní prvky
    if getattr(meta, "inners", None):
        for inner_meta in meta.inners:
            # Cesta k privátnímu slotu inneru (např. "_motor")
            inner_name = inner_meta.name_private
            inner_instance = getattr(obj, inner_name)
            fill_random(inner_instance, retries=retries, allow_locked=allow_locked)
        return obj

    # 2) Atomická / kompozitní hodnota → generujeme
    #    (obj je AtomInstanceProtocol nebo CompositeInstanceProtocol)
    if not allow_locked and getattr(obj, "_locked", False):
        # Zamčené prvky přeskočíme
        return obj

    value_type: ValidTypes = meta.value_type

    for _ in range(retries):
        value = generate_random_value_for_type(value_type, meta)

        try:
            # Použijeme plnou pipeline: normalize + setter
            cls = obj.__class__
            normalized = cls.normalize(value, process_none=True)
            obj.value = normalized
            return obj
        except Exception:
            # Hodnota neprošla → zkusíme znovu
            continue

    raise ValueError(
        f"Cannot generate valid random value for {obj!r} "
        f"of type {value_type!r} after {retries} attempts."
    )


# ---------------------------------------------------------
# Generátor hodnot podle typu + metadat
# ---------------------------------------------------------

def generate_random_value_for_type(
    type_: ValidTypes,
    meta: "SimpleMetadataLike",
) -> Any:
    """
    Vygeneruje náhodnou hodnotu podle typu a metadat.

    - Respektuje registr TYPE_GENERATORS.
    - Umí pracovat s UnionType, Optional, Enum, list/dict.
    - Pro kompozice může použít logic/decompose, pokud je to vhodné.
    """

    # 1) Uživatelský generátor pro celý typ
    if type_ in TYPE_GENERATORS:
        return TYPE_GENERATORS[type_]()

    # 2) UnionType (např. int | str, Optional[int] apod.)
    if isinstance(type_, UnionType):
        return _generate_for_union(type_, meta)

    # 3) Jednoduché built-in typy
    if type_ is int:
        return random.randint(0, 1000)

    if type_ is float:
        return round(random.uniform(0.0, 1000.0), 2)

    if type_ is str:
        length = random.randint(5, 15)
        alphabet = string.ascii_letters + string.digits
        return "".join(random.choices(alphabet, k=length))

    if type_ is bool:
        return random.choice([True, False])

    if type_ is datetime:
        start = datetime(2020, 1, 1)
        end = datetime(2025, 12, 31)
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    if type_ is date:
        start = date(2020, 1, 1)
        end = date(2025, 12, 31)
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    if type_ is Path:
        name = "".join(random.choices(string.ascii_lowercase, k=10))
        return Path(f"/tmp/{name}.txt")

    # 4) Enum typy
    if isinstance(type_, type) and issubclass(type_, Enum):
        return random.choice(list(type_))

    # 5) Generické typy (list[T], dict[K, V]) – přes __origin__ / __args__
    origin = getattr(type_, "__origin__", None)
    args = getattr(type_, "__args__", ())

    if origin is list:
        item_type = args[0] if args else int
        length = random.randint(1, 5)
        return [generate_random_value_for_type(item_type, meta) for _ in range(length)]

    if origin is dict:
        key_type = args[0] if args else str
        val_type = args[1] if len(args) > 1 else int
        length = random.randint(1, 5)
        return {
            generate_random_value_for_type(key_type, meta):
            generate_random_value_for_type(val_type, meta)
            for _ in range(length)
        }

    # 6) Kompozitní typy – pokud metadata naznačují kompozici
    #    (meta.inners, meta.logic, meta.decompose, meta.is_decomposeable)
    if getattr(meta, "inners", None) and getattr(meta, "is_decomposeable", False):
        # Pokusíme se vytvořit hodnotu přes logic/decompose:
        # - vygenerujeme náhodné hodnoty pro inners
        # - zavoláme cls.calculate_value(...) nebo meta.logic(...)
        # Tady ale nemáme přímo cls, takže použijeme fallback:
        return _generate_composite_value_from_inners(meta)

    # 7) Fallback – použij default, pokud je definován
    default = getattr(meta, "default", None)
    if default is not None:
        return default

    # 8) Poslední fallback – None (nevalidní, ale retry mechanismus to řeší)
    return None


# ---------------------------------------------------------
# Pomocné generátory pro Union / Optional / Composite
# ---------------------------------------------------------

def _generate_for_union(
    union_type: UnionType,
    meta: "SimpleMetadataLike",
) -> Any:
    """
    Vygeneruje hodnotu pro UnionType (např. int | str, Optional[int]).

    - Pokud Union obsahuje None → občas vrátí None.
    - Jinak náhodně vybere jeden z typů a vygeneruje hodnotu pro něj.
    """

    # Rozpad UnionType na jednotlivé typy
    # (UnionType.__args__ existuje od Pythonu 3.10)
    args = getattr(union_type, "__args__", None)
    if not args:
        return None

    # Optional[T] → Union[T, None]
    has_none = any(t is type(None) for t in args)
    non_none_types = [t for t in args if t is not type(None)]

    # Občas vrátíme None, pokud je povolené
    if has_none and random.random() < 0.3:
        return None

    # Vybereme náhodný typ z non-none variant
    chosen = random.choice(non_none_types)
    return generate_random_value_for_type(chosen, meta)


def _generate_composite_value_from_inners(
    meta: "SimpleMetadataLike",
) -> Any:
    """
    Pokusí se vytvořit kompozitní hodnotu na základě inners.

    - Vygeneruje náhodné hodnoty pro každý inner podle jeho value_type.
    - Vrátí tuple nebo dict podle toho, jak uživatel typově modeluje kompozici.
    - Je to heuristický fallback – skutečná logika je v _logic/_decompose.
    """

    inners = getattr(meta, "inners", None)
    if not inners:
        return None

    # Jednoduchý heuristický model:
    # - pokud value_type je tuple → vrátíme tuple hodnot
    # - pokud value_type je dict  → vrátíme dict name->value
    # - jinak vrátíme tuple hodnot
    value_type = getattr(meta, "value_type", None)

    values: list[Any] = []
    for inner_meta in inners:
        inner_type = inner_meta.value_type
        inner_value = generate_random_value_for_type(inner_type, inner_meta)
        values.append(inner_value)

    origin = getattr(value_type, "__origin__", None)
    args = getattr(value_type, "__args__", ())

    if value_type is tuple or origin is tuple:
        return tuple(values)

    if value_type is dict or origin is dict:
        # mapujeme podle jmen inners
        return {
            inner_meta.name_snake: val
            for inner_meta, val in zip(inners, values)
        }

    # Fallback – tuple hodnot
    return tuple(values)


# ---------------------------------------------------------
# Pomocné API pro testy – naplnění celého stromu
# ---------------------------------------------------------

def fill_random_tree(
    root: "SimpleInstanceLike",
    *,
    retries: int = 5,
    allow_locked: bool = False,
) -> "SimpleInstanceLike":
    """
    Ergonomický alias pro fill_random – explicitně říká, že naplňuje celý strom.

    V praxi je totožný s fill_random(root), ale můžeš ho použít v testech
    pro lepší čitelnost.
    """
    return fill_random(root, retries=retries, allow_locked=allow_locked)
