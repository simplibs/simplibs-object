from typing import TypeAlias, Any, Callable


# Type for operator from the operator module
UnaryOperator: TypeAlias = Callable[[Any], Any]