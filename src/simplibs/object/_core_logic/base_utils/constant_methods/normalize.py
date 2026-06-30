from typing import Any, TYPE_CHECKING
# Inners
from .validations import raise_missing_value_error
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def normalize(
    cls: "SimpleConstantProtocol",
    value: Any,
    *,
    process_none: bool = False
) -> Any:
    """
    Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleLogicError.

    Pravidla:
    1. Pokud je value None a process_none=True -> vrací default.
    2. Pokud je value None a process_none=False -> vyvolá chybu.
    3. Pokud je value rovna defaultu -> vrací instanci defaultu (šetří paměť).
    4. Ostatní hodnoty jsou validovány a vráceny v původní podobě.
    """

    # 1. Ošetření None
    if value is None:

        # 1.1 Vyřízení pokud je None očekáváné
        if process_none:
            return cls.meta.default

        # 1.2 Vyovální výjimky
        raise_missing_value_error(cls)

    # 2. Ošetření situace kdy je hodnota schodná s defaultní
    # noinspection PyBroadException
    try:

        # 2.1 Pokud hodnota odpovídá defaultu - vrací se odkaz na default
        if value == cls.meta.default:
            return cls.meta.default

    # 2.2 Pokud hodnota není porovnatelná - pokračuje se na validaci
    except Exception:
        pass

    # 3. Validace
    cls.validate(value)

    # 4. Navrácení zvalidvoané hodnoty
    return value

