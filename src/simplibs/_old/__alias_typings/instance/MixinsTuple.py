from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...mixins.base_class import SimpleMixinLike


# Reprezentuje n-tici mixinů aplikovaných na danou instanci nebo třídu
MixinsTuple: TypeAlias = tuple["SimpleMixinLike", ...]