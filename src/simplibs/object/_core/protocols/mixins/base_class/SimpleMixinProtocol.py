from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ...instance import SimpleInstanceLike
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import ValidTypes


@runtime_checkable
class SimpleMixinProtocol(
    SimpleInstanceLike,
    Protocol
):
    """
    Protocol representing the foundational interface for all mixins in the Simple system.

    Declares the presence of the initialization hook and configuration flags
    that control which instance types a mixin can be applied to within the factory.
    """

    # --- DECLARATIVE MIXIN CONSTRAINTS (Class-level configuration) ---
    _constant_only: bool
    _composite_only: bool
    _mutable_only: bool
    _immutable_only: bool
    _only_types: "ValidTypes"

    # --- INITIALIZATION LOGIC ---
    def init_mixins(self) -> None:
        """
        Anchor for reactive mixin initialization.

        Implementations are expected to call super().init_mixins() to pass
        control to the next mixin or base class along the MRO chain.
        """
        ...

    @staticmethod
    def __extend_instance_class__(instance_cls: "SimpleInstanceLike") -> "SimpleInstanceLike":
        """
        Optional hook enabling a mixin to modify the instance class
        prior to runtime instance creation (e.g., attaching dynamic properties).
        """
        ...

    __name__: str