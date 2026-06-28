from typing import Any, TYPE_CHECKING
from collections.abc import Callable
# Anotations
if TYPE_CHECKING:
    from ..protocols.classes import SimpleBaseProtocol


class SimpleSettings:

    # Nastavení logeru
    logger: Callable[["SimpleBaseProtocol", Any], None] | None = None