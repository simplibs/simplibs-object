from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...classes import SimpleClassLike


# Represents a tuple of inner components declared within a composition
InnersTuple: TypeAlias = tuple["SimpleClassLike", ...]