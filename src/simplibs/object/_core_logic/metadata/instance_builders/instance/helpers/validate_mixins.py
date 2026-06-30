from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ......mixins.base_class import SimpleMixin
# Inners
from .validations.mixins import (
    validate_mixin_is_simple_base_subclass,
    validate_mixin_is_class,
    raise_mixin_not_allowed_for_mutable,
    raise_mixin_not_allowed_for_immutable,
    raise_mixin_not_allowed_for_constant,
    raise_mixin_not_support_default_value_type,
    raise_mixin_not_allowed_for_composite
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol
    from ......protocols.alias_typings import MixinsTuple


def validate_mixins(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    is_atom: bool,
    mutable: bool = True,
) -> None:
    """
    Validuje všechny mixiny před sestavením instanční třídy.

    - Ověří, že každý mixin je platná třída a potomek SimpleMixin.
    - Kontroluje deklarativní omezení mixinů:
        * _constant_only      → povolené pouze pro atomické instance
        * _composite_only     → povolené pouze pro kompozitní instance
        * _mutable_only       → povolené pouze pro mutable instance
        * _immutable_only     → povolené pouze pro immutable instance
        * _only_types         → povolené pouze pro defaultní hodnoty určitého typu
    - Při porušení pravidel vyvolá odpovídající validační výjimku.
    """

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