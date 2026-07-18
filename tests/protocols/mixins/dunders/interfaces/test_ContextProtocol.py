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
    Protokol pro mixin Context.

    Garantuje podporu pro kontextové řízení (with obj:), což umožňuje
    bezpečné ohraničení kódu. Vstup do kontextu vrací samotnou instanci (Self).
    """

    def __enter__(self) -> Self:
        """
        Vstup do kontextového bloku 'with'.
        Vrací samotnou instanci objektu pro přiřazení (with obj as x:).
        """
        ...

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[False]:
        """
        Ukončení kontextového bloku 'with'.

        Přebírá případné informace o výjimce. Vždy vrací False, což zajišťuje, 
        že výjimky nejsou potlačeny a propagují se standardně dál.
        """
        ...