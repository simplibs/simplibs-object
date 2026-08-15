from typing import Protocol, runtime_checkable, Self, Literal, Type
from types import TracebackType
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ContextProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Context mixin.

    Guarantees support for context management (with obj:), enabling safe code
    scoping. Entering the context returns the instance itself (Self).
    """

    def __enter__(self) -> Self:
        """
        Enters the 'with' context block.
        Returns the object instance itself for assignment (with obj as x:).
        """
        ...

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[False]:
        """
        Exits the 'with' context block.

        Receives potential exception details. Always returns False, ensuring
        exceptions are never swallowed and propagate normally.
        """
        ...