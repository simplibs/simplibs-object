import logging
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..protocols.classes import SimpleClassType

_logger = logging.getLogger("simple")


def log_value_event(
    cls: "SimpleClassType",
    value: Any,
    event: str  # "set" | "recalculate"
) -> None:
    """Centrální místo pro všechna logovací volání knihovny."""

    from .SimpleSettings import SimpleSettings  # lazy import — vyhne se circular importu

    # 1. Stdlib logging
    if _logger.isEnabledFor(logging.DEBUG):
        _logger.debug(
            "[%s] %s = %r",
            event,  # "set" nebo "recalculate"
            cls.__name__,
            value
        )

    # 2. Volitelný uživatelský callback
    if SimpleSettings.on_value_change:
        SimpleSettings.on_value_change(cls, value, event)