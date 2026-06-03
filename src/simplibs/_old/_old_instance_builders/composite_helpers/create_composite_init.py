from typing import Callable
# Outers
from ...._types import SimpleMetaType


def create_composite_init(
    meta: SimpleMetaType,
    base_class_name: str
) -> Callable:
    """
    Vytvoří univerzální inicializační metodu pro kompozitní instanci.
    Zrodí všechny přímé vnitřní prvky (inners) a prováže je s touto kompozicí.
    """

    def __init__(self):
        # 1. Zavoláme init předka (AtomBase)
        # Ten nastaví základní self._value a self._owner = None
        super(self.__class__, self).__init__()

        # 2. Projdeme všechny přímé inners definované v metadatech
        for inner in meta.inners:
            inner_meta = inner.meta

            # Zjistíme živou instanční třídu pro tento pod-prvek
            # (buď atom_class nebo composite_class z jeho metadat)
            inner_instance_cls = inner_meta.atom_class if inner_meta.is_constant else inner_meta.composite_class

            # Zrodíme čistou instanci tohoto vnitřního prvku (zcela bez parametrů)
            inner_instance = inner_instance_cls()

            # Provážeme ji: nastavíme ji jako vlastníka tuto naši kompozici
            inner_instance._owner = self

            # Uložíme ji do příslušného privátního slotu (např. self._motor)
            setattr(self, inner_meta.name_private, inner_instance)

        # 3. Odstartujeme inicializační kaskádu pro případné mixiny kompozice
        self.init_mixins()

    # Nastavení správných jmen pro debugování a introspekci
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    return __init__
