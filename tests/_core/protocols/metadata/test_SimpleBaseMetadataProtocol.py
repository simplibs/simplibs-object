from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..classes import SimpleClassLike
    from ..alias_typings import NamesTuple, NamesSet


@runtime_checkable
class SimpleBaseMetadataProtocol(
    Protocol
):
    """
    Protocol for foundational metadata shared across all Simple classes.

    Provides core naming identity (class_name, name_tuple, name_snake, name_private),
    namespace registry management (node_names_set), blueprint path calculation,
    and the hook for subclass-specific user data processing (_process_user_data).
    """

    # 1. Reference to the owner class
    owner_class: "SimpleClassLike"

    # 2. Name identity
    class_name: str
    name_tuple: "NamesTuple"
    name_snake: str
    name_private: str

    # 3. Namespace management
    node_names_set: "NamesSet"

    # 4. Auxiliary pre-computation for __repr__
    blueprint_path: str

    def _process_user_data(self) -> None:
        """Initialization hook for subclasses to process user-defined data."""
        ...