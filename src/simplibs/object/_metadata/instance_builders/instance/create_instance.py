from typing import Any
# Outers
from ...._types import SimpleClassType
from ...constants import BASE_CLASS_NAMES
# Inners
from .validations.parameters import validate_param_is_bool, validate_class_is_not_base_class
from .validations.mixins import validate_mixin_is_simple_base_subclass, validate_mixin_is_compatible, validate_mixin_is_class
from .validations.slots import raise_mixin_slots_conflict_error


def create_instance(
    cls: SimpleClassType,
    mixins: tuple,
    as_atom: bool
) -> Any:
    """Kompletní orchestrace validace a sestavení nové runtime instance."""

    # 1. Validace třídy a bool parametru
    if (cls.__name__ in BASE_CLASS_NAMES or
        not isinstance(as_atom, bool)):
        validate_class_is_not_base_class(cls)
        validate_param_is_bool(as_atom)

    # 2. Získání základní třídy a určení režimu (Atom / Composite)
    is_atom = cls.meta.is_constant or as_atom
    base_class = cls.meta.atom_class if is_atom else cls.meta.composite_class

    # 3. Kontrola mixinů
    for mixin in mixins:
        from ....mixins.base_class import SimpleMixin
        # Ověření, že jde o třídu a že je to potomek SimpleMixin
        if (not isinstance(mixin, type) or
            not issubclass(mixin, SimpleMixin) or
            (is_atom and getattr(mixin, "_composite_only", False))):
            validate_mixin_is_class(cls, mixin)
            validate_mixin_is_simple_base_subclass(cls, mixin)
            validate_mixin_is_compatible(cls, mixin, is_atom)


    # 4. Příprava dat pro sestavení třídy
    class_parents = (*mixins, base_class)
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = {"__slots__": ()}

    # 5. Sestavení instanční třídy (Chráněno před konflikty slotů)
    try:
        _instance_cls = type(class_name, class_parents, class_dict)
    except TypeError as error:
        # Python sám vyhodí TypeError, pokud dojde ke kolizi slotů mezi mixiny navzájem
        raise_mixin_slots_conflict_error(cls, mixins, error)

    # 6. Přepis jména třídy
    # noinspection PyUnboundLocalVariable
    _instance_cls.__qualname__ = class_name

    # 7. Doplnění třídní logiky
    for mixin in mixins:
        if hasattr(mixin, "__extend_instance_class__"):
            _instance_cls = mixin.__extend_instance_class__(_instance_cls)

    # 8. Vytvoření živé instance a její inicializace
    # noinspection PyTypeChecker
    instance = object.__new__(_instance_cls)
    # noinspection PyArgumentList
    instance.__init__()

    # 9. Navrácení vytvořené instance
    return instance

