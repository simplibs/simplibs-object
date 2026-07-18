from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ....exceptions import SimpleError
# inners
from .validations import raise_unexpected_validation_error, raise_validation_error
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def validate(
    cls: "SimpleConstantProtocol",
    value: Any,
    *,
    return_bool: bool = False
) -> bool | None | NoReturn:
    """
    Provede kompletní validační řetězec. Vrací True, False nebo vyvolá výjimku.

    Řetězec se skládá z:
    1. Typové validace (ValidateType.validate_type)
    2. Uživatelské validace (definované v _validate)
    """

    # 1. Validace typu a validační metodou
    try:
        result = (
            cls.validate_type(value, return_bool=return_bool) and
            cls.meta.validate(value, return_bool=return_bool)
        )

    # 2. Zpracování výjimek
    except Exception as e:

        # 2.1 Vyřízení pro bool odpověd
        if return_bool:
            return False

        # 2.2 Zpracování definované výjimky
        if isinstance(e, SimpleError):
            raise

        # 2.3 Zpracování ostatních výjimmek
        raise_unexpected_validation_error(cls, value, e)

    # 3. Kontrola výsledku (případné vyvolání výjimky)
    if result is False and return_bool is False:
        raise_validation_error(cls, value)

    # 4. Navrácen bool odpovědi
    return result
