from typing import Any
import inspect
from simplibs.sentinels import UNSET
# Outers
from ...._types import MetaType
# inners
from .utils.collect_composite_parameters import collect_composite_parameters


class CompositeParamsMixin:
    """
    Mixin poskytující přístup k dynamicky generované COMPOSITE_PARAMS.
    """

    # Definice používaných prvků
    meta: MetaType

    # noinspection PyPep8Naming
    @classmethod
    def COMPOSITE_PARAMS(cls) -> list[inspect.Parameter]:
        """
        Vrací seznam parametrů (inspect.Parameter) pro celou kompozici.
        """

        # 1. Načtení hodnoty z metadat
        cached_class = cls.meta.composite_params

        # 2. Pokud date existuí vrací se
        if cached_class is not UNSET:
            return cached_class

        # 3. Vypočítání hodnoty
        composite_params = [cls.meta.atom_param]
        inners = getattr(cls.meta, 'inners', [])
        for inner in inners:
            composite_params.extend(inner.COMPOSITE_PARAMS())

        # 4. Uložení do metadat
        cls.meta.composite_params = composite_params

        # 5. Navrácení třídy
        return composite_params
