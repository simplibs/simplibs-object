from typing import Callable, Any


class SimpleSettings:

    # Nastavení logeru
    logger: Callable[[type, Any], None] | None = None