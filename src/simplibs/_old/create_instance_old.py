from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from .....mixins.base_class import SimpleMixin
from ...constants import BASE_CLASS_NAMES
# Inners
from .validations.parameters import validate_param_is_bool, validate_class_is_not_base_class
from .validations.mixins import (
    validate_mixin_is_simple_base_subclass,
    validate_mixin_is_class,
    raise_mixin_not_allowed_for_mutable,
    raise_mixin_not_allowed_for_immutable,
    raise_mixin_not_allowed_for_constant,
    raise_mixin_not_support_default_value_type,
    raise_mixin_not_allowed_for_composite
)
from .validations.slots import raise_mixin_slots_conflict_error
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.instance import SimpleInstanceLike
    from .....protocols.mixins.base_class import SimpleMixinProtocol
    from .....protocols.alias_typings import MixinsTuple


def create_instance(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    *,
    as_atom: bool,
    mutable: bool = True,
    validate: bool = True
) -> Any:
    """Kompletní orchestrace validace a sestavení nové runtime instance."""

    # 1. Validace třídy a parametrů
    if validate:
        if (cls.__name__ in BASE_CLASS_NAMES or
            not isinstance(as_atom, bool)):
            validate_class_is_not_base_class(cls)
            validate_param_is_bool(as_atom)

    # 2. Určení režimu (atom / composite) a kontrola imutability hodnotyx
    is_atom = cls.meta.is_constant or as_atom
    if not mutable:
        try:
            return hash(cls.meta.default)
        except TypeError:
            raise TypeError(
                f"Immutable instance '{cls.meta.class_name}' "
                f"cannot wrap non-hashable default value"
            )

    # 3. Výběr základní třídy podle režimu a mutability
    if is_atom:
        base_class = (
            cls.meta.atom_class_mutable
            if mutable else
            cls.meta.atom_class_immutable
        )
    else:
        base_class = (
            cls.meta.composite_class_mutable
            if mutable else
            cls.meta.composite_class_immutable
        )

    # 4. Kontrola mixinů
    if validate:

        for mixin in mixins:

            if (not isinstance(mixin, type) or
                not issubclass(mixin, SimpleMixin)):
                validate_mixin_is_class(cls, mixin)
                validate_mixin_is_simple_base_subclass(cls, mixin)

            mixin: SimpleMixinProtocol

            # noinspection PyProtectedMember
            if mixin._constant_only and not is_atom:
                raise_mixin_not_allowed_for_composite(cls, mixin)

            # noinspection PyProtectedMember
            if mixin._composite_only and is_atom:
                raise_mixin_not_allowed_for_constant(cls, mixin)

            # noinspection PyProtectedMember
            if mixin._mutable_only and not mutable:
                raise_mixin_not_allowed_for_immutable(cls, mixin)

            # noinspection PyProtectedMember
            if mixin._immutable_only and mutable:
                raise_mixin_not_allowed_for_mutable(cls, mixin)

            # noinspection PyProtectedMember
            if mixin._only_types is not UNSET and not isinstance(cls.meta.default, mixin._only_types):
                raise_mixin_not_support_default_value_type(cls, mixin)

    # 5. Příprava dat pro sestavení třídy
    class_parents = (*mixins, base_class)
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = {
        "__slots__": (),
        "__is_constant__": is_atom,
        "__is_mutable__": mutable,
        "__mixins__": mixins
    }

    # 6. Sestavení instanční třídy (Chráněno před konflikty slotů)
    try:
        # noinspection PyTypeChecker
        _instance_cls = type(
            class_name,
            class_parents,
            class_dict
        )
    except TypeError as error:
        raise_mixin_slots_conflict_error(cls, mixins, error)

    # 7. Přepis jména třídy
    # noinspection PyUnboundLocalVariable
    _instance_cls.__qualname__ = class_name

    # 8. Aplikace mixinů
    for mixin in mixins:
        if hasattr(mixin, "__extend_instance_class__"):
            _instance_cls = mixin.__extend_instance_class__(_instance_cls)

    # 9. Vytvoření instance
    instance = object.__new__(_instance_cls)

    # 10. Inicializace instance
    # composite init i atom init už mají parametr mutable zabudovaný v sobě
    instance.__init__()

    # 11. Navrácení vytvořené instance
    instance: "SimpleInstanceLike"
    return instance
