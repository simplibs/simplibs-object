from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...classes import SimpleClassLike


# Rychlá mapa pro vyhledání vnitřní třídy podle jejího snake_case jména
InnersMap: TypeAlias = dict[str, "SimpleClassLike"]