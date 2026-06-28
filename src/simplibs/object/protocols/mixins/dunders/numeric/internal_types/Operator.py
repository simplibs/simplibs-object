from typing import TypeAlias, Any
from collections.abc import Callable


# Typ pro operator z modulu operator
Operator: TypeAlias = Callable[[Any, Any], Any]