from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def exception_info_for_default(
    owner_class: "SimpleClassLike",
):
    attribute_name = "_default"
    class_name = owner_class.__name__
    class_parrent = "SimpleObject" if "SimpleObject" in owner_class.__mro__ else "SimpleConstant"
    error_name = "INVALID DEFAULT DEFINITION"
    context = f"Kontrola a validace metadat pro: {class_name}.{attribute_name}"

    return class_name, class_parrent, error_name, context