from typing import Any, Callable
from .is_lambda import is_lambda


def process_decompose(decompose: Any):

    if not is_lambda(decompose):
        return decompose

    def _decompose(cls, value):
        return decompose(value)

    return _decompose
