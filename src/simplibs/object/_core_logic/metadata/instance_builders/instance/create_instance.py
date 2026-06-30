from typing import Any, TYPE_CHECKING
# Inners
from .helpers import (
    validate_mixins,
    get_base_class,
    validate_hashing_for_immutable_value,
    validate_class_and_parameters,
    create_instance_class
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.instance import SimpleInstanceLike
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
        validate_class_and_parameters(cls, as_atom, mutable)

    # 2. Určení režimu (atom / composite)
    is_atom = cls.meta.is_constant or as_atom

    # 3. Kontrola imutability hodnoty
    if not mutable:
        validate_hashing_for_immutable_value(cls)

    # 4. Výběr základní třídy podle režimu a mutability
    base_class = get_base_class(cls, is_atom, mutable)

    # 5. Kontrola mixinů
    if validate:
        validate_mixins(cls, mixins, is_atom, mutable)

    # 6. Sestavení instanční třídy
    _instance_cls = create_instance_class(cls, mixins, base_class, is_atom, mutable)

    # 7. Aplikace mixinů
    for mixin in mixins:
        if hasattr(mixin, "__extend_instance_class__"):
            _instance_cls = mixin.__extend_instance_class__(_instance_cls)

    # 8. Vytvoření instance
    instance = object.__new__(_instance_cls)

    # 9. Inicializace instance
    # composite init i atom init už mají parametr mutable zabudovaný v sobě
    instance.__init__()

    # 10. Navrácení vytvořené instance
    instance: "SimpleInstanceLike"
    return instance
