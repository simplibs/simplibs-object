# Outers
from ......._types import SimpleClassType


def exception_info_for_type(
    owner_class: SimpleClassType,
):
    attribute_name = "_type"
    class_name = owner_class.__name__
    class_parrent = "SimpleObject" if "SimpleObject" in owner_class.__mro__ else "SimpleConstant"
    error_name = "INVALID TYPE DEFINITION"
    context = f"Kontrola a validace metadat pro: {class_name}.{attribute_name}"
    acceptable_definitions = (
        "Acceptable definitions:",
        f"class {class_name}({class_parrent}):",
        f"    {attribute_name}: type = samostatně definované typy jako je 'str', 'int', atd.",
        f"    {attribute_name}: UnionType = union type definice pro více povolených typů.",
        f"    {attribute_name}: tuple[type, ...] = tuple obsahujích více povolených typů (bude převedeno na UnionType).",
        "    ...",
    )
    return class_name, class_parrent, error_name, context, acceptable_definitions