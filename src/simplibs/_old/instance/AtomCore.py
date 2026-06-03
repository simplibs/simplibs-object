from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ....._types import MetaType
# inners
from .utils.make_atom_core_class import make_atom_core_class


class AtomCoreMixin:
    """
    Mixin poskytující přístup k dynamicky generované ATOM_CORE třídě.
    """

    # Definice používaných prvků
    meta: MetaType

    # noinspection PyPep8Naming
    @classmethod
    def ATOM_CORE(cls) -> type:
        """
        Vrací třídu jádra. Používá caching v metadatech pro eliminaci
        opakovaného vytváření třídy.
        """

        # 1. Načtení hodnoty z metadat
        cached_class = cls.meta.core_class

        # 2. Pokud date existuí vrací se
        if cached_class is not UNSET:
            return cached_class

        # 3. Vypočítání třídy
        core_class = make_atom_core_class(cls)

        # 4. Uložení do metadat
        cls.meta.core_class = core_class

        # 5. Navrácení třídy
        return core_class