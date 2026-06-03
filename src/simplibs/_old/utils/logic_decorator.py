import inspect
from typing import Callable
from functools import wraps

from simplibs.exception import SimpleException


def logic_decorator(
    *inners,
    return_type: type,
) -> Callable:
    """
    Dekorátor sestavující inspect.Signature pro metodu _logic SimpleObject třídy.

    Sestaví signaturu z předaných inner tříd a návratového typu.
    Validaci správnosti hodnot zajišťují metadata SimpleObject třídy.

    Args:
        *inners: Inner třídy nebo tuple inner tříd (_inners, *_inners nebo inner1, inner2, ...).
        return_type: Návratový typ signatury (_type nebo konkrétní typ z tuple typů).

    Example:
        @classmethod
        @logic_decorator(*_inners, return_type=_type)
        def _logic(cls, **kwargs): ...
    """

    # 1. Normalizace inners — akceptuje tuple i rozbalené hodnoty
    if len(inners) == 1 and isinstance(inners[0], tuple):
        resolved_inners = inners[0]
    else:
        resolved_inners = inners

    # 2. Vytažení parametrů z inner tříd
    parameters = [
        inner.meta.atom_param_signature
        for inner in resolved_inners
    ]

    # 3. Zpracování návratového typu
    if isinstance(return_type, tuple):
        raise SimpleException(
            error_name="INVALID ARGUMENT ERROR",
            value_label="return_type",
            value=return_type,
            expected="A single type (e.g. int, str, MyClass)",
            problem="'return_type' cannot be a tuple — _logic must have a single, explicit return type.",
            how_to_fix=(
                "If '_type' is a tuple, pick the primary return type explicitly:",
                "  @logic_decorator(*_inners, return_type=int)",
                "  @logic_decorator(*_inners, return_type=float)",
            ),
            context="logic_decorator — return_type check",
            exception=TypeError
        )
    return_annotation = return_type

    # 4. Sestavení signatury
    signature = inspect.Signature(
        parameters=parameters,
        return_annotation=return_annotation,
        __validate_parameters__=False
    )

    # 5. Definice a navrácení dekorátoru
    def decorator(function: Callable) -> Callable:

        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        wrapper.__signature__ = signature
        return wrapper

    return decorator