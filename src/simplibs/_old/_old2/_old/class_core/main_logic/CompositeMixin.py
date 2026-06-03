from .SimpleInstance import SimpleInstance
from inspect import Signature, Parameter

# noinspection PyPep8Naming
class SimpleMixin(SimpleInstance):


    @classmethod
    def MIXIN(cls):
        """Vrátí instanční třídu složenou z mixinů všech inners."""
        return cls._get_or_make_cache_attr(
            cache_attr="mixin_class",
            method_name="make_mixin_class"
        )

    @classmethod
    def make_mixin_class(cls):
        """Vytvoří mixin třídu složenou z vlastní mixin a mixinů všech inners."""

        # Navrácení mixin pokud není žádný inners (jedná se o atom)
        # if not cls.meta.inners or cls.meta.as_atom == True:
        if not cls.meta.inners:
            return cls.INSTANCE()

        # Složení mixinů všech inners rekurzivně
        inner_classes = tuple(
            inner.MIXIN() for inner in cls.meta.inners
        )

        # Složení signatur
        def __init__(self, **kwargs):
            super(type(self), self).__init__(**kwargs)

        # Podpis pro IDE a našeptávače
        __init__.__signature__ = Signature(cls.MIXIN_PARAMS())

        # Předci: Aktuální instance + všechny inners
        class_parents = (cls.INSTANCE(),) + inner_classes

        # Název nové třídy (I s přímími inners pro lepší IDE a nintrospekci)
        mixin_names = [inner.__name__ for inner in  cls.meta.inners]
        class_name = f"{cls.__name__}Mixin({'_'.join(mixin_names)})"

        # Slovník nové třídy
        class_dict = {
            '__doc__': f"Kompozitní mixin třídy {cls.__name__} složená z: {', '.join(mixin_names)}",
            '__slots__': (),
            '__init__': __init__,
        }

        # Vytvoření nové třídy
        mixin_class = type(class_name, class_parents, class_dict)
        return mixin_class
