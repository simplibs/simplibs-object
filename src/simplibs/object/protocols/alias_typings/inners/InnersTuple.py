from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...classes import SimpleClassLike


# Reprezentuje n-tici vnitřních komponent deklarovaných v kompozici
InnersTuple: TypeAlias = tuple["SimpleClassLike", ...]