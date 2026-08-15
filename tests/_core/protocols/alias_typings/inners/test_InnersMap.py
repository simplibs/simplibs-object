from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...classes import SimpleClassLike


# Fast mapping lookup for retrieving an inner class by its snake_case name
InnersMap: TypeAlias = dict[str, "SimpleClassLike"]