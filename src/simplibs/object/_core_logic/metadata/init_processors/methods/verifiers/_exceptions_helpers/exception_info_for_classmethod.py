# Outers
from ......protocols import ClassMethodProtocol
# Inners
from .exception_context_for_classmethod import exception_context_for_classmethod


def exception_info_for_classmethod(
    bound_method: ClassMethodProtocol,
    expected_params: tuple[str, ...],
    expected_args_params_count: int
):

    # 1. Získání základních informací
    class_name, method_name, context = exception_context_for_classmethod(bound_method)
    class_parrent = "SimpleObject" if "SimpleObject" in bound_method.__self__.__mro__ else "SimpleConstant"

    # 2. Rozdělení parametrů na args a kwargs
    args_params = ', '.join(expected_params[:expected_args_params_count])
    kwargs_param = ', '.join(expected_params[expected_args_params_count:])

    # 3. Vytvoření popisu parametrů
    params = f"{args_params}" + (f", *, {kwargs_param}" if kwargs_param else "")

    # 4. Vytvoření výstupu pro očakávanou strukturu v chybovém oznamu
    excepted_structure = (
        "Expected structure:",
        f"class {class_name}({class_parrent}):",
        "    ...",
        "    @classmethod",
        f"    def {method_name}({params}):",
        "        ..."
    )

    # 5. Navrácení vypočtených hodnot
    return {
        "class_name": class_name,
        "method_name": method_name,
        "excepted_structure": excepted_structure,
        "context": context
    }

