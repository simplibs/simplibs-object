# Outers
from .......protocols import SimpleMetadataType, SimpleMetaProtocol
# Inners
from .make_value_getter_only_on_class import make_value_getter_only_on_class
from .remove_mutable_methods import remove_mutable_methods

def make_all_inners_value_getter_only(meta: SimpleMetadataType) -> None:
    """
    Rekurzivně projde celý strom inners a na jejich třídách
    přepíše .value property na getter-only.
    """

    for inner in meta.inners:

        # Vytaření proměných
        inner_meta = inner.meta

        # 1) Přepsat .value na třídě inneru
        make_value_getter_only_on_class(inner_meta.composite_class)
        remove_mutable_methods()

        # 2) Rekurzivně pokračovat dál pro kompozice
        if not inner_meta.is_constant:
            make_all_inners_value_getter_only(inner_meta)
