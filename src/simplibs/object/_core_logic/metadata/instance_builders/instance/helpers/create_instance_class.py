from typing import TYPE_CHECKING
# Inners
from .validations.slots import raise_mixin_slots_conflict_error
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.instance import SimpleInstanceLike
    from ......protocols.classes import SimpleClassLike
    from ......protocols.instance.core_classes import AtomInstanceProtocol, CompositeInstanceProtocol
    from ......protocols.alias_typings import MixinsTuple
    from ......protocols.instance import SimpleInstanceLike


def create_instance_class(
    cls: "SimpleClassLike",
    mixins: "MixinsTuple",
    base_class: "AtomInstanceProtocol | CompositeInstanceProtocol",
    is_atom: bool,
    mutable: bool
) -> "SimpleInstanceLike":
    """
    Sestaví novou instanční třídu pro runtime instanci.

    - Kombinuje zvolené mixiny a základní instanční třídu (`base_class`)
      do výsledného MRO.
    - Vytvoří dynamickou třídu pomocí `type()`, včetně technických atributů:
        * __slots__        – prázdné, aby mixiny mohly přidávat vlastní
        * __is_constant__  – režim atom/composite
        * __is_mutable__   – režim mutability
        * __mixins__       – tuple použitých mixinů
    - Ošetřuje konflikty slotů mezi mixiny a základní třídou.
    - Přepisuje __qualname__ pro čistší reprezentaci.
    - Vrací vytvořenou instanční třídu (nikoliv instanci).
    """

    # 1. Příprava dat pro sestavení třídy
    class_parents = (*mixins, base_class)
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = {
        "__slots__": (),
        "__is_constant__": is_atom,
        "__is_mutable__": mutable,
        "__mixins__": mixins
    }

    # 2. Sestavení instanční třídy (Chráněno před konflikty slotů)
    try:
        # noinspection PyTypeChecker
        _instance_cls = type(
            class_name,
            class_parents,
            class_dict
        )
    except TypeError as error:
        raise_mixin_slots_conflict_error(cls, mixins, error)

    # 3. Přepis jména třídy
    # noinspection PyUnboundLocalVariable
    _instance_cls.__qualname__ = class_name

    # 4. Vrácení vytvořené třídy
    _instance_cls: "SimpleInstanceLike"
    # noinspection PyUnboundLocalVariable
    return _instance_cls