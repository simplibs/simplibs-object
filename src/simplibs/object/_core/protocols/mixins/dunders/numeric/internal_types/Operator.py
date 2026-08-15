from typing import TypeAlias, Any, Callable


# Type for operator from the operator module
Operator: TypeAlias = Callable[[Any, Any], Any]