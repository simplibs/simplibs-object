from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ....._types import MetaType
# inners
from .utils.make_core_class import make_atom_core_class


class SimpleCoreMixin:

    # Definice používaných prvků
    meta: MetaType

    # noinspection PyPep8Naming
    @classmethod
    def CORE(cls):
        """Vytvoří mixin"""
        cached_val = cls.meta.core_class
        if cached_val is not UNSET:
            return cached_val
        core_class = make_atom_core_class(cls)
        cls.meta.core_class = core_class
        return core_class




    # noinspection PyPep8Naming
    @classmethod
    def CORE(cls):
        """Vytvoří mixin"""
        return cls._get_or_make_cache_attr(
            cache_attr="core_class",
            method_name="make_core"
        )


    @classmethod
    def make_atom_core(cls):

        # 1. Definice vnitřních funkcí
        def __init__(self, new_value: Any = None):
            self._value = self.normalize(new_value, process_none=True)

        def getter(self) -> Any:
            return self._value

        def setter(self, new_value: Any) -> None:
            self._value = self.normalize(new_value, process_none=True)

        # 2. Název nové třídy
        class_name = f"{cls.__name__}Atom"

        # 3. Předci třídy z kterých dědí
        class_parents = (SimpleBase,)

        # 4. Slovník nové třídy - všimni si přidání 'value'
        class_dict = {
            '__doc__': f"{class_name} – hodnotové jádro pro {cls.meta.name_readable}",
            '__slots__': ("_value",),
            '__init__': __init__,
            'value': property(getter, setter),
        }

        # 5. Vytvoření nové třídy
        core_class = type(class_name, class_parents, class_dict)
        return core_class
