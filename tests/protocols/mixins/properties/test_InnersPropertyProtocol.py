from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..base_class import SimpleMixinProtocol
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


@runtime_checkable
class InnersPropertyProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin InnersProperty.

    Indikuje, že kompozitní instance byla dynamicky rozšířena o properties
    pro přímý komfortní přístup k jejím vnitřním prvkům (inners)
    na základě definice blueprintu.
    """

    # Samotný mixin nemá sloty, properties jsou generovány až za běhu.

    def __getattr__(self, name: str) -> "SimpleInstanceLike":
        """
        Dynamický fallback pro přístup k vygenerovaným vlastnostem vnitřních prvků.

        Garantuje, že jakýkoliv dynamicky stažený prvek (sub-kompozice nebo atom)
        splňuje základní instanční rozhraní.
        """
        ...