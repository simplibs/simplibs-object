from textwrap import dedent
from typing import Any, Callable


def make_composite_init(owner_class: SimpleClassProtocol) -> Callable:
    meta = owner_class.meta

    # 1. Sběr informací o parametrech (kdo má decompose?)
    # Pro zjednodušení teď předpokládejme, že v initu chceme
    # hlavní hodnotu (pokud je decompose) a všechny přímé inners.
    params = []
    if meta.has_decompose:
        params.append(meta.name_snake)

    for inner in meta.inners:
        params.append(inner.meta.name_snake)

    # 2. Příprava těla - Inicializace slotů
    # Musíme vytvořit Core instance pro VŠECHNY zúčastněné sloty
    all_slots = [meta] + [inner.meta for inner in meta.inners]

    init_body = []
    for m in all_slots:
        # Vytvoření core objektu s výchozí hodnotou (None)
        init_body.append(f"self.{m.name_private} = {m.name_snake}_core(None)")

    # 3. Aplikace hodnot z argumentů (Logika priorit)
    # Pokud přišel hlavní parametr a má dekompozici, má přednost
    if meta.has_decompose:
        main = meta.name_snake
        init_body.append(f"if {main} is not None:")
        init_body.append(f"    self.{main} = {main}")
        init_body.append("else:")
        # Pokud není hlavní, zkusíme inners
        for inner in meta.inners:
            p = inner.meta.name_snake
            init_body.append(f"    if {p} is not None: self.{p} = {p}")
    else:
        # Pokud není dekompozice, hlavní parametr v initu ani není
        for inner in meta.inners:
            p = inner.meta.name_snake
            init_body.append(f"if {p} is not None: self.{p} = {p}")

    # 4. Sestavení zdrojového kódu
    sig_params = ", ".join([f"{p}=None" for p in params])
    source = dedent(f'''
    def __init__(self, {sig_params}) -> None:
        # Inicializace všech Core objektů do slotů
        {chr(10).join("        " + line for line in init_body)}
    ''')

    # 5. Namespace pro exec
    namespace = {f"{m.name_snake}_core": m.core_class for m in all_slots}
    exec(source, namespace)
    return namespace["__init__"]


def make_composite_class(owner_class: SimpleClassProtocol) -> type:
    meta = owner_class.meta

    # 1. Sesbíráme všechny sloty a properties (pro sebe i inners)
    all_metas = [meta] + [inner.meta for inner in meta.inners]

    class_dict = {
        '__doc__': f"Kompozice {owner_class.__name__}",
        '__slots__': tuple(m.name_private for m in all_metas),
        '__init__': make_composite_init(owner_class),
        '__allow_instantiation__': True,
    }

    # 2. Přidáme property pro každý prvek (včetně sebe sama)
    for m in all_metas:
        def make_props(current_meta=m):
            def getter(self):
                return getattr(self, current_meta.name_private)

            def setter(self, val):
                core_obj = getattr(self, current_meta.name_private)
                core_obj.value = val
                self._on_update()  # Tady se spustí přepočet logic/decompose

            return property(getter, setter)

        class_dict[m.name_snake] = make_props()

    # 3. Vytvoření třídy
    class_name = f"{owner_class.__name__}Composition"
    # Dědíme už jen z báze, která umí _on_update
    return type(class_name, (AtomInstanceBase,), class_dict)