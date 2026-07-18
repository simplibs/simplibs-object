from typing import TypeAlias, TYPE_CHECKING
from collections.abc import Mapping
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


# Rychlá mapa pro přímý přístup k živé instanci sub-nodu podle jeho snake_case názvu
NodesInstanceDict: TypeAlias = Mapping[str, "SimpleInstanceLike"]