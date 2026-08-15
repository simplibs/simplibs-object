from typing import Any, Callable
from .is_lambda import is_lambda


def process_logic(logic: Any, params_name: tuple[str, ...]):

    if not is_lambda(logic):
        return logic

    params = ", ".join(params_name)
    src = f"""def _logic(cls, {params}): return logic({params})"""
    namespace = {"logic": logic}
    exec(src, namespace)

    return namespace["_logic"]