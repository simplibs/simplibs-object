from typing import TYPE_CHECKING
# Outers
from ....base_utils.properties import create_constant_property
# Inners
from .InstanceBase import InstanceBase
from .helpers import create_atom_init, create_root_value_setter
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import AtomInstanceProtocol


def make_atom_class(
    meta: SimpleMetadataLike,
    *,
    mutable:bool = True
) -> "AtomInstanceProtocol":

    # 1. Defnice jména třídy
    base_class_name = (
        f"{meta.class_name}AtomMutableBase"
        if mutable else
        f"{meta.class_name}AtomImmutableBase"
    )

    # 2. Definice předků třídy
    class_parents = (InstanceBase, meta.owner_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Atomický instanční objekt pro {meta.class_name}",
        "__slots__": ("_value", "_owner", "_locked"),
        "__init__": create_atom_init(meta, base_class_name),
        "value": create_constant_property(meta, mutable=mutable),
        "owner": property(lambda self: self._owner, doc="Reference na nadřazenou kompozici.")
    }

    # 4. Případné doplnění mutable položek
    if mutable:
        class_dict["_root_value_setter"] = create_root_value_setter(meta, base_class_name)

    # 5. Vytvoření třídy
    # noinspection PyTypeChecker
    atom_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 6. Odstranění deklarativních atributů
    for name in ("_type", "_default", "_validate", "bool_or_raise_validate_error"):
        if name in atom_class.__dict__:
            delattr(atom_class, name)

    # 7. Navrácení třídy
    atom_class: "AtomInstanceProtocol"
    return atom_class


