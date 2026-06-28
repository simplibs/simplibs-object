from typing import TypeAlias, Any
from types import EllipsisType


# Vstupní hodnota pro krok: buď konkrétní hodnota, nebo ... (Ellipsis) pro výchozí krok
StepValue: TypeAlias = Any | EllipsisType