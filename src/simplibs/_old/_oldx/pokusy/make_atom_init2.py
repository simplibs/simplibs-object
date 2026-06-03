from textwrap import dedent
# Outers
from ...._types import (
    SimpleMetaType,
    SimpleClassProtocol,
)


def make_init(
    owner_class: SimpleClassProtocol
) -> callable:
    """
    Dynamicky vytvoří inicializační metodu
    pro ATOMIC instance třídu.
    """

    # Metadata
    meta: SimpleMetaType = owner_class.meta

    # Data
    attr_name: str = meta.name_private
    param_name: str = meta.name_snake
    param_type: type = meta.value_type
    core_class: type = meta.core_class
    class_name: str = owner_class.__name__

    # Název typu pro anotaci
    type_name: str = param_type.__name__

    # Zdrojový kód
    source = dedent(f'''
    def __init__(
        self,
        {param_name}: {type_name} | None = None
    ) -> None:
        """
        Inicializační metoda pro třídu {class_name}.
        """

        self.{attr_name} = core_class({param_name})
    ''')

    # Namespace
    namespace = {
        type_name: param_type,
        "core_class": core_class,
    }

    # Vytvoření funkce
    exec(source, namespace)

    # Vrácení funkce
    return namespace["__init__"]