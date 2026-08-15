from typing import Any


def is_lambda(fn: Any):
    return callable(fn) and fn.__name__ == "<lambda>"
