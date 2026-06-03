from typing import Any
# Outers
from ...._types import SimpleClassProtocol
from .utils2.create_property import create_property


def make_atom_class(
    owner_class: type
) -> type:
    """
    Továrna na instance, vytváří finální třídu, kterou uživatel používá.
    """

    # 1. Příprava dat
    docstring = f"Instanční objekt pro {owner_class.__name__}"
    slots = ("_value", "__weakref__")
    init = create_init_for_atom(owner_class)
    repr = create_repr_for_atom(owner_class)
    value_propety = create_property("_value", owner_class)

    # 2. Sestavení třídy
    class_name = f"{owner_class.__name__}Instance"
    class_parents = (InstanceBase, owner_class,)
    class_dict = {
        '__doc__': docstring,
        '__slots__': slots,
        '__init__': init,
        '__repr__': repr,
        'value': value_propety,
    }

    # 7. Vytvoření a navrácení ohbjektu
    return type(class_name, class_parents, class_dict)