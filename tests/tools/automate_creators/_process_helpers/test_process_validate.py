from typing import Any, Callable
from .is_lambda import is_lambda


def process_validate(validate: Any):

    if not is_lambda(validate):
        return validate

    # If user provided a lambda or simple function, wrap it
    def _validate(cls, value: Any, *, return_bool: bool = False):
        return validate(value)

    return _validate
