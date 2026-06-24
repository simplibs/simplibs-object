from typing import Protocol
# Outers
from ..instance import (
    SimpleCompositeInstanceProtocol,
    SimpleInstanceProtocol
)
from ..mixins.base_class import SimpleMixinProtocol

class SimpleInstanceType(
    SimpleCompositeInstanceProtocol,
    SimpleInstanceProtocol,
    SimpleMixinProtocol,
    Protocol
):
    pass

