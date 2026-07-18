from typing import TYPE_CHECKING
from collections.abc import Callable
# Inners
from ._get_inner_instance_class import _get_inner_instance_class
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance.core_classes import CompositeInstanceProtocol


def create_composite_init(
    meta: "SimpleMetadataLike",
    base_class_name: str,
    *,
    mutable: bool = True
) -> Callable:
    """
    Vytvoří univerzální inicializační metodu pro kompozitní instanci.
    Zrodí všechny přímé vnitřní prvky (inners) a prováže je s touto kompozicí.
    """


    def __init__(
        self: "CompositeInstanceProtocol"
    ) -> None:
        # 1. Zavoláme init předka (AtomBase)
        # Ten nastaví základní self._value a self._owner = None
        if mutable:
            # noinspection PyArgumentList
            meta.atom_class_mutable.__init__(self)
        else:
            # noinspection PyArgumentList
            meta.atom_class_immutable.__init__(self)

        # 2. Projdeme všechny přímé inners definované v metadatech
        for inner in meta.inners:
            inner_meta = inner.meta

            # Zjistíme živou instanční třídu pro tento pod-prvek
            # (buď atom_class nebo composite_class z jeho metadat)
            inner_instance_cls = _get_inner_instance_class(inner_meta, mutable)

            # Zrodíme čistou instanci tohoto vnitřního prvku (zcela bez parametrů)
            inner_instance = inner_instance_cls()

            # Provážeme ji: nastavíme ji jako vlastníka tuto naši kompozici
            inner_instance._owner = self

            # Uložíme ji do příslušného privátního slotu (např. self._motor)
            setattr(self, inner_meta.name_private, inner_instance)

    # Nastavení správných jmen pro debugování a introspekci
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    return __init__
