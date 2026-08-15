from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...mixins.base_class import SimpleMixinLike


# Represents a tuple of mixins applied to a given instance or class
MixinsTuple: TypeAlias = tuple["SimpleMixinLike", ...]