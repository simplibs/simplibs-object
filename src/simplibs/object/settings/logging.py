import logging
from typing import Any, TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from ..protocols.classes import SimpleClassType

# Interní logger knihovny
_logger = logging.getLogger("simple")

# Volitelný callback pro reakci na změnu hodnoty.
# Nastavení: import simplibs.object.settings.logging as simple_logging
#             simple_logging.on_value_change = lambda cls, value, event: ...
on_value_change: Callable[["SimpleClassType", Any, str], None] | None = None


def log_value_event(
    cls: "SimpleClassType",
    value: Any,
    event: str
) -> None:
    """Centrální místo pro všechna logovací volání knihovny."""

    # 1. Stdlib logging
    if _logger.isEnabledFor(logging.DEBUG):
        _logger.debug(
            "[%s] %s = %r",
            event,
            cls.__name__,
            value
        )

    # 2. Volitelný uživatelský callback
    if on_value_change is not None:
        # noinspection PyCallingNonCallable
        on_value_change(cls, value, event)