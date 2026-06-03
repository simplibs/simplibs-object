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
    attr_name = meta.name_private
    param_name = meta.name_snake
    param_type = meta.value_type
    core_class = meta.core_class
    class_name = owner_class.__name__

    # Source
    source = dedent(f'''
    def __init__(
        self,
        {param_name}: param_type | None = None
    ) -> None:
        """
        Inicializační metoda pro třídu {class_name}.
        """

        self.{attr_name} = core_class({param_name})
    ''')

    # Namespace
    namespace = {
        "param_type": param_type,
        "core_class": core_class,
    }

    # Compile
    exec(source, namespace)

    # Return function
    return namespace["__init__"]