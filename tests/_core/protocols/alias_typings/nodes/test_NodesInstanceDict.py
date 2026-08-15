from typing import TypeAlias, TYPE_CHECKING
from collections.abc import Mapping
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


# Fast map for direct access to live subnode instance by its snake_case name
NodesInstanceDict: TypeAlias = Mapping[str, "SimpleInstanceLike"]