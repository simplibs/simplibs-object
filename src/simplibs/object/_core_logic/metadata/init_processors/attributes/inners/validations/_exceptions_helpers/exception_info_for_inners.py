# Outers
from .......protocols import SimpleClassType


def exception_info_for_inners(
    owner_class: SimpleClassType,
):
    class_name = owner_class.__name__
    error_name = "INVALID INNERS DEFINITION"
    context = f"Kontrola a validace metadat pro: {class_name}._inners"
    acceptable_definitions = (
        "Acceptable definitions:",
        f"class {class_name}(SimpleObject):",
        f"    _inners: tuple = (PrvekA, PrvekB)",
        "    ...",
    )
    return class_name, error_name, context, acceptable_definitions