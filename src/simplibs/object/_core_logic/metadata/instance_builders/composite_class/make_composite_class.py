from typing import TYPE_CHECKING
# Outers
from ....base_utils.properties import create_composite_property
# Inners
from .helpers import (
    create_composite_init,
    create_recalculate_self,
    create_recalculate_inners,
    create_properties_for_inners
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import CompositeInstanceProtocol


def make_composite_class(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True
) -> "CompositeInstanceProtocol":
    """
    Orchestrátor pro tvorbu kompozitní instanční třídy (Node).
    Vytváří mutable nebo immutable variantu podle parametru `mutable`.
    """

    # 1. Definice jména třídy
    base_class_name = (
        f"{meta.class_name}CompositeMutableBase"
        if mutable else
        f"{meta.class_name}CompositeImmutableBase"
    )

    # 2. Definice předků třídy
    base_class = meta.atom_class_mutable if mutable else meta.atom_class_immutable
    class_parents = (base_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Kompozitní instanční objekt pro {meta.class_name}",
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name, mutable=mutable),
        "value": create_composite_property(meta, mutable=mutable),
    }

    # 4. Přidání property pro přímé inners
    class_dict |= create_properties_for_inners(meta, mutable=mutable)

    # 5. Mutable-only metody
    if mutable:
        class_dict["_recalculate_self"] = create_recalculate_self(meta, base_class_name)
        class_dict["_recalculate_inners"] = create_recalculate_inners(meta, base_class_name)

    # 6. Vytvoření třídy
    # noinspection PyTypeChecker
    composite_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 7. Odstranění deklarativních atributů
    for name in ("inners", "_logic", "_decompose"):
        if name in composite_class.__dict__:
            delattr(composite_class, name)

    # 8. Navrácení třídy
    composite_class: "CompositeInstanceProtocol"
    return composite_class
