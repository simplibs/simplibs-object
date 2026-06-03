# Outers
from ..._types import SimpleMetaType
# Inners
from .InstanceBase import InstanceBase
from .atom_helpers import (
    create_atom_init,
    create_atom_value_property,
    create_root_value_setter
)


def make_atom_class(
    meta: SimpleMetaType
) -> type:

    # 1. Defnice jména třídy
    base_class_name = f"{meta.class_name}AtomBase"

    # 2. Definice předků třídy
    class_parents = (InstanceBase, meta.owner_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Atomický instanční objekt pro {meta.class_name}",
        "__slots__": ("_value", "_owner"),
        "__init__": create_atom_init(meta, base_class_name),
        "_root_value_setter": create_root_value_setter(meta, base_class_name),
        "value": create_atom_value_property(meta),
        "owner": property(lambda self: self._owner, doc="Reference na nadřazenou kompozici.")
    }

    # 4. Vytvoření třídy
    atom_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 5. Odstranění deklarativních atributů
    for name in ("_type", "_default", "_validate", "bool_or_raise_validate_error"):
        if hasattr(atom_class, name):
            delattr(atom_class, name)

    # 6. Navrácení třídy
    return atom_class


