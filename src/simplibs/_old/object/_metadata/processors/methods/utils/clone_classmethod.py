from typing import Callable
from types import FunctionType

# noinspection PyUnresolvedReferences
def clone_classmethod(cm: classmethod) -> classmethod:
    """
    Přijme classmethod (např. výstup getattr(owner_class, name))
    a vrátí nový, plně oddělený classmethod objekt.
    """

    # 1. Získání func
    func = cm.__func__

    # 2. Vytvoření nové funkce
    new_func: Callable = FunctionType(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__,
    )

    # 3. Přenos anotací
    new_func.__annotations__ = dict(func.__annotations__)

    # 4. Přenos keyword-only defaultů
    if func.__kwdefaults__:
        new_func.__kwdefaults__ = dict(func.__kwdefaults__)
    else:
        new_func.__kwdefaults__ = None

    # 5. Přenos vlastních atributů funkce (pokud nějaké jsou)
    if func.__dict__:
        new_func.__dict__.update(func.__dict__)

    # 6. Vrátíme nový classmethod descriptor
    return classmethod(new_func)
