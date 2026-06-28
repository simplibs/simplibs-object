from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def exception_context_for_classmethod(
    bound_method: "ClassMethodProtocol",
):

    # 1. Jméno třídy a metody
    class_name = bound_method.__self__.__name__
    method_name = bound_method.__func__.__name__

    # 2. Definice pro kontext chybového oznamu
    context = f"Kontrola a validace metadat pro: {class_name}.{method_name}"

    # 3. Navrácení vypočtených hodnot
    return {
        "class_name": class_name,
        "method_name": method_name,
        "context": context
    }