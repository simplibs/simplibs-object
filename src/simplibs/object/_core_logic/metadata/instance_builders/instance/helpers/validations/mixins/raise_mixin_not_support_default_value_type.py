from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike
    from ........protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_not_support_default_value_type(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    ...