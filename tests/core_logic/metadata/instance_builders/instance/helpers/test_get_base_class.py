from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.instance.core_classes import AtomInstanceProtocol, CompositeInstanceProtocol


def get_base_class(
    cls: "SimpleClassLike",
    is_atom: bool,
    mutable: bool,
) -> "AtomInstanceProtocol | CompositeInstanceProtocol":
    """
    Vrátí správnou instanční základní třídu podle režimu a mutability.

    - Pokud je instance atomická → použije atom_class_mutable / atom_class_immutable.
    - Pokud je instance kompozitní → použije composite_class_mutable / composite_class_immutable.
    - Výběr je plně řízen metadaty definované třídy (`cls.meta`).
    """

    if is_atom:
        return (
            cls.meta.atom_class_mutable
            if mutable else
            cls.meta.atom_class_immutable
        )
    else:
        return (
            cls.meta.composite_class_mutable
            if mutable else
            cls.meta.composite_class_immutable
        )