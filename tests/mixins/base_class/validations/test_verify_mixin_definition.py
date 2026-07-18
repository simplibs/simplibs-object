from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from ..._common.constants import FORBIDDEN_NAMES
from .errors import (
    raise_mixin_slots_is_not_defined,
    raise_mixin_slots_unsuport_type,
    raise_mixin_slots_contains_forbidden_slot_names,
    raise_mixin_dict_contains_forbidden_attributes,
    raise_mixin_slots_contain_unvalid_type,
    raise_mixin_init_mixins_missing_super_call
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.base_class import SimpleMixinProtocol



def verify_mixin_definition(
    cls: "SimpleMixinProtocol"
) -> None:

    # 1. Validace přístomnosti slotu
    if "__slots__" not in cls.__dict__:
        raise_mixin_slots_is_not_defined(cls)

    # 2. Vytvoření proměné
    slots = cls.__dict__["__slots__"]

    # 3. Validace typu slotu
    if not isinstance(slots, (tuple, str)):
        raise_mixin_slots_unsuport_type(cls)

    # 4. Validace zda všechny prvky jsou str
    slots_set = set(slots) if isinstance(slots, tuple) else {slots}
    if not all(isinstance(s, str) for s in slots_set):
        raise_mixin_slots_contain_unvalid_type(cls)

    # 5. Validace zda některý z prvků není zakázaný
    if FORBIDDEN_NAMES & slots_set:
        raise_mixin_slots_contains_forbidden_slot_names(cls)

    # 6. Validace zda nejsou na třídě definované třídní atributy s nepovolenými jmény
    if FORBIDDEN_NAMES & cls.__dict__.keys():
        raise_mixin_dict_contains_forbidden_attributes(cls)

    # 7. Validace zda _composite_only je v případě definice uživatelem zapsán jako bool
    for flag in ("_constant_only", "_composite_only", "_mutable_only", "_immutable_only"):
        if flag in cls.__dict__ and not isinstance(cls.__dict__[flag], bool):
            raise TypeError(
                f"Mixin {cls.__name__}: deklarativní flag '{flag}' musí být typu bool."
            )

    # 7.y Validace _only_types
    if "_only_types" in cls.__dict__:
        only = cls.__dict__["_only_types"]

        # UNSET je povolená hodnota
        if only is UNSET:
            pass

        # type je povolený
        elif isinstance(only, type):
            pass

        # tuple typů je povolený
        elif (
            isinstance(only, tuple)
            and all(isinstance(t, type) for t in only)
        ):
            pass

        # Union typ je povolený
        elif getattr(only, "__origin__", None) is Union:
            pass

        # jinak → chyba
        else:
            raise TypeError(
                f"Mixin {cls.__name__}: hodnota '_only_types' musí být type, tuple[type,...], Union[...] nebo UNSET."
            )

    # 8. Validace přítomnosti super() v metodě init_mixins
    if "init_mixins" in cls.__dict__:
        func = cls.__dict__["init_mixins"]

        # 8.1 Získání všech jmen (funkcí/atributů) volaných uvnitř metody
        called_names = func.__code__.co_names

        # 8.2 Pro správné řetězení musíme najít jak 'super', tak název metody 'init_mixins'
        if "super" not in called_names or "init_mixins" not in called_names:
            raise_mixin_init_mixins_missing_super_call(cls)