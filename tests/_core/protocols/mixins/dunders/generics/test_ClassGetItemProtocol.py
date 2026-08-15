from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ClassGetItemProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the ClassGetItem mixin.

    Guarantees support for class-level generic indexing (e.g., MyClass[int]),
    enabling clean usage of advanced type hints without runtime penalties.
    """

    def __class_getitem__(cls, item: Any) -> type:
        """
        Special dunder method supporting generic syntax on the class.
        Returns either the superclass result or the class object (type) itself.
        """
        ...