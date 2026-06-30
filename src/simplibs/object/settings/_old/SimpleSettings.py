import logging
from typing import Any, TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from ..protocols.classes import SimpleClassType

# Interní logger knihovny — vytvoří se jednou, globálně
_library_logger = logging.getLogger("simple")


class SimpleSettings:
    """
    Globální nastavení knihovny Simple.

    Logování:
        Knihovna používá stdlib logging pod jménem 'simple'.
        Pro zapnutí stačí nastavit level na kořenovém loggeru:

            import logging
            logging.getLogger("simple").setLevel(logging.DEBUG)

        Pro vlastní handler (např. do souboru):

            handler = logging.FileHandler("simple.log")
            logging.getLogger("simple").addHandler(handler)

        Pro vlastní callback (pokročilé použití):

            SimpleSettings.on_value_change = lambda cls, value, event: print(...)
    """

    # --- Logování přes stdlib ---
    log_level: int = logging.NOTSET  # NOTSET = knihovna sama nic nenastavuje

    # --- Volitelný callback pro pokročilé použití ---
    on_value_change: Callable[["SimpleClassType", Any, str], None] | None = None


# Použití :
# setter
log_value_event(cls, value, event="set")

# _recalculate_self (pokud chceš logovat i přepočty)
log_value_event(cls, value, event="recalculate")