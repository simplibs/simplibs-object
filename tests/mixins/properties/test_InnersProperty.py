from typing import TYPE_CHECKING
# Outers
from ..base_class import SimpleMixin
# Inners
from ._utils.inners_property import collect_all_nested_properties
# Annotations
if TYPE_CHECKING:
    from ...protocols.instance import SimpleInstanceLike


class InnersProperty(SimpleMixin):
    """
    Mixin přidávající property na vnitřní prvky.

    Dynamicky rozšiřuje kompozitní instance o properties
    pro přímý komfortní přístup k jejím vnitřním prvkům (inners)
    na základě definice blueprintu.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Hook pro úpravu instanční třídy
    # ----------------------------------------

    @staticmethod
    def __extend_instance_class__(
        instance_cls: "SimpleInstanceLike"
    ) -> "SimpleInstanceLike":
        """
        Interní metoda pro připojení prvků k třídě, před inicializačním procesem.
        """

        # 1. Vytvoření potřebných properties
        nested_props = collect_all_nested_properties(instance_cls.meta)

        # 2. Připojení atributů k třídě
        for name, prop in nested_props.items():
            setattr(instance_cls, name, prop)

        # 3. Navrácení pozměněné třídy
        return instance_cls