from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ...._types import MetaType
# inners
from .utils.make_atom_instance_class import make_atom_instance_class


class AtomInstanceMixin:
    """
    Mixin poskytující přístup k dynamicky generované ATOM_INSTANCE třídě.
    """

    # Definice používaných prvků
    meta: MetaType

    # noinspection PyPep8Naming
    @classmethod
    def ATOM_INSTANCE(cls) -> type:
        """
        Vrací třídu pro atomické instance. Používá caching v metadatech pro eliminaci
        opakovaného vytváření třídy.
        """

        # 1. Načtení hodnoty z metadat
        cached_class = cls.meta.instance_class

        # 2. Pokud date existuí vrací se
        if cached_class is not UNSET:
            return cached_class

        # 3. Vypočítání třídy
        instance_class = make_atom_instance_class(cls)

        # 4. Uložení do metadat
        cls.meta.instance_class = instance_class

        # 5. Navrácení třídy
        return instance_class
