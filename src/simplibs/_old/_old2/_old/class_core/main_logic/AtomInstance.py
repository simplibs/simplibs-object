from inspect import Signature, Parameter
from .SimpleCore import SimpleCore
from .mixins.instance.InstanceBase import InstanceBase


# noinspection PyPep8Naming
class SimpleInstance(SimpleCore):

    @classmethod
    def INSTANCE(cls):
        """Vytvoří instance"""
        return cls._get_or_make_cache_attr(
            cache_attr="instance_class",
            method_name="make_atomic_instance"
        )

    @classmethod
    def get_signature(cls):
        return Signature([
            Parameter(
                cls.meta.name_snake,
                Parameter.KEYWORD_ONLY,
                default=None,
                annotation=cls.meta.value_type
            )
        ])

    # noinspection PyTypeChecker
    @classmethod
    def make_atomic_instance(cls):
        """
        Vytvoří atomický instance pro tento SimpleObject.
        Tento instance neřeší inners, jen jeden parametr podle attr_name a param_name.
        """

        # Názvy atributů a parametrů
        attr_name = cls.meta.name_private
        param_name = cls.meta.name_snake
        CoreClass = cls.CORE()

        # 1. Definice vnitřních funkcí
        def __init__(self, **kwargs):
            value = kwargs.get(param_name)
            setattr(self, attr_name, CoreClass(value))

            # Definice aby při přimýchání do mixinu byli předány kwargs dál ostatním v řetězci MRO!.
            super(type(self), self).__init__(**kwargs)

        def getter(self):
            # Vrací celý objekt Atomu
            return getattr(self, attr_name)

        def setter(self, value):
            # Nastaví hodnotu do Atomu a vyvolá update hook
            getattr(self, attr_name).value = value
            self._on_update()

        # Podpis pro IDE a našeptávače
        __init__.__signature__ = Signature([cls.meta.atom_param_signature])

        # Název nové třídy
        class_name = f"{cls.__name__}Instance"

        # Předci třídy z kterých dědí
        class_parents = (InstanceBase,)

        # Slovník nové třídy
        class_dict = {
            '__doc__': f"{class_name} – atomická instance pro {cls.meta.name_readable}",
            '__slots__': (attr_name,),
            '__init__': __init__,
            param_name: property(getter, setter),
        }

        # Vytvoření nové třídy
        instance_class = type(class_name, class_parents, class_dict)
        return instance_class