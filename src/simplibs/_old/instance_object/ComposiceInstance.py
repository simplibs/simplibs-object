from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ....._types import MetaType
# inners
from .utils.make_composition_instance_class import make_composition_instance_class


class ComposiceInstanceMixin:
    """
    Mixin poskytující přístup k dynamicky generované COMPOSICE_INSTANCE třídě.
    """

    # Definice používaných prvků
    meta: MetaType

    # noinspection PyPep8Naming
    @classmethod
    def COMPOSICE_INSTANCE(cls) -> type:
        """
        Vrací třídu pro kompozitní instance. Používá caching v metadatech pro eliminaci
        opakovaného vytváření třídy.
        """

        # 1. Načtení hodnoty z metadat
        cached_class = cls.meta.composition_class

        # 2. Pokud date existuí vrací se
        if cached_class is not UNSET:
            return cached_class

        # 3. Vypočítání třídy
        composition_class = make_composition_instance_class(cls)

        # 4. Uložení do metadat
        cls.meta.composition_class = composition_class

        # 5. Navrácení třídy
        return composition_class

