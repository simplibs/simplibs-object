from typing import TypeAlias, Any
from collections.abc import Callable


# Typ pro operator z modulu operator
UnaryOperator: TypeAlias = Callable[[Any], Any]