from typing import Optional, Any
from .SimpleMixin import SimpleMixin
from .utils.determine_atom_mode import determine_atom_mode
from .utils.process_mixins import process_mixins


# noinspection PyPep8Naming
class SimpleObject(SimpleMixin):

    @classmethod
    def OBJECT(cls, *mixins: Any, use_defaults: bool =True, as_atom: bool = None):
        """
        Vrátí koncovou třídu.
        Pokud jsou použity parametry, generuje se třída dynamicky bez trvalého uložení do cache.
        """
        # Pokud je voláno bez parametrů, zkusíme cache
        if as_atom is None and not mixins:
            return cls._get_or_make_cache_attr(
                cache_attr="object_class",
                method_name="make_object_class"
            )

        # Pokud uživatel něco specifikoval, vyrobíme to čerstvé
        return cls.make_object_class(*mixins, use_defaults=use_defaults, as_atom=as_atom)

    @classmethod
    def make_object_class(cls, *mixins: Any, use_defaults: bool =True, as_atom: bool = None):
        """Továrna na koncové objekty."""

        # Určení režimu (Atom vs Mixin)
        is_atom = determine_atom_mode(cls, as_atom)

        # Výběr základního kamene
        ObjectBase = cls.INSTANCE() if is_atom else cls.MIXIN()

        # Vyřešíme mixiny skrze orchestrátor
        ObjectMixins = process_mixins(mixins, use_defaults=use_defaults)

        # Předci: Vybraná báze + náš velký koncový mixin se schopnostmi
        class_parents = ObjectMixins + (ObjectBase,)

        # Název nové třídy
        class_name = f"{cls.__name__}Object"

        # Slovník nové třídy
        class_dict = {
            '__doc__': f"Koncový objekt {cls.__name__} (Atom: {is_atom}, Mixins: {mixins})",
            '__slots__': (),
        }

        # Vytvoření nové třídy
        object_clas = type(class_name, class_parents, class_dict)
        return object_clas
