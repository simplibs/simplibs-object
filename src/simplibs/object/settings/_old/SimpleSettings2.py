from typing import Any, TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ..protocols.classes import SimpleClassType


class SimpleSettings:

    # Nastavení logeru
    logger: Callable[["SimpleClassType", Any], None] | None = None