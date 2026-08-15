from typing import TypeAlias, Any
from types import EllipsisType


# Input step value: either a specific numeric value, or ... (Ellipsis) for the default step size
StepValue: TypeAlias = Any | EllipsisType