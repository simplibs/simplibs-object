from typing import TypeAlias, Any
from collections.abc import Callable


# Callback/Akce spuštěná při dosáhnutí limitu (přijímá instanci/hodnotu nebo Unset)
LimitAction: TypeAlias = Callable[..., Any] | Any