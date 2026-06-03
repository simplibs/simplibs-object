from typing import Any, NoReturn
# Inners
from .validations import raise_type_error


def validate_type(
    cls,
    value: Any,
    *,
    return_bool: bool = False
) -> bool | NoReturn:
    """
    Provede deterministickou validaci typu na základě metadat třídy.
    """

    # 1. Validace Happy path
    if isinstance(value, cls.meta.value_type):
        return True

    # 2. Vrácení bool negace
    if return_bool:
        return False

    # 3. Vyvolání výjimky
    raise_type_error(cls, value, cls.meta.value_type)
