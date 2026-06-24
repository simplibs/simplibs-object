from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..classes import SimpleClassLike


@runtime_checkable
class SimpleBaseMetadataProtocol(
    Protocol
):

    # 1. Reference na třídu vlastníka
    owner_class: "SimpleClassLike"

    # 2. Názvová identita
    class_name: str
    name_tuple: tuple[str, ...]
    name_snake: str
    name_private: str

    # 3. Správa jmenného prostoru
    node_names_set: set[str]

    # 4. Pomocný předvýpočet pro __repr__
    blueprint_path: str

    def _process_user_data(self) -> None:
        """Inicializační hook pro podtřídy."""
        ...