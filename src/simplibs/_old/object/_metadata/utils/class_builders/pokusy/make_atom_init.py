import keyword
from textwrap import dedent


def make_init(
    *,
    attr_name: str,
    param_name: str,
    param_type: type,
    core_class: type,
    class_name: str,
) -> callable:

    # Validace názvu parametru
    if not param_name.isidentifier():
        raise ValueError(
            f"Invalid parameter name: {param_name!r}"
        )

    if keyword.iskeyword(param_name):
        raise ValueError(
            f"Parameter name cannot be keyword: {param_name!r}"
        )

    # Název typu pro anotaci
    type_name = param_type.__name__

    # Zdrojový kód metody
    source = dedent(f'''
    def __init__(
        self,
        {param_name}: {type_name} | None = None
    ) -> None:
        """
        Initializační metoda pro třídu {class_name}.
        """

        self.{attr_name} = core_class({param_name})
    ''')

    # Namespace pro exec
    namespace = {
        type_name: param_type,
        "core_class": core_class,
    }

    # Vytvoření funkce
    exec(source, namespace)

    # Vrácení vytvořené funkce
    return namespace["__init__"]