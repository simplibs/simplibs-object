# Outers
from ...._types import SimpleMetaType
# Inners
from .InstanceBase import InstanceBase
from .atom_helpers.create_init import create_init
from .atom_helpers.create_repr import create_repr
from .property_helpers.create_atom_property import create_atom_property


def make_atom_class(
    meta: SimpleMetaType
) -> type:

    # 1. Defnice jména třídy
    class_name = meta.instance_name

    # 2. Definice předků třídy
    class_parents = (InstanceBase, meta.owner_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Atomický instanční objekt pro {meta.class_name}",
        "__slots__": ("_value", "_owner"),
        "__init__": create_init(meta),
        "__repr__": create_repr(meta),
        "value": create_atom_property(meta),
    }

    # 4. Vytvoření a nevrácení třídy
    return type(
        class_name,
        class_parents,
        class_dict
    )